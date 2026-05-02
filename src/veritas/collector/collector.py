from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .mmr import MerkleMountainRange


FS_SYSCALLS = {"write", "pwrite64", "truncate", "renameat2", "mkdirat", "unlinkat", "sendfile"}
PROC_SYSCALLS = {"clone", "clone3", "execve", "execveat", "exit_group"}
CAPTURE_SYSCALLS = FS_SYSCALLS | PROC_SYSCALLS


@dataclass(slots=True)
class CanonicalEvent:
    sequence_number: int
    monotonic_timestamp_ns: int
    pid: int
    tid: int
    syscall: str
    arguments_hash: str
    return_value: int


class CollectorAbort(Exception):
    pass


class Collector:
    def __init__(self) -> None:
        self.session_uuid = str(uuid.uuid4())
        self.mmr = MerkleMountainRange()
        self._seq = 0

    @staticmethod
    def _args_hash(arguments: dict[str, Any]) -> str:
        packed = json.dumps(arguments, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.blake2s(packed).hexdigest()

    def canonicalize(self, raw_event: dict[str, Any]) -> CanonicalEvent | None:
        syscall = str(raw_event["syscall"])
        if syscall not in CAPTURE_SYSCALLS:
            return None
        self._seq += 1
        return CanonicalEvent(
            sequence_number=self._seq,
            monotonic_timestamp_ns=int(raw_event["monotonic_timestamp_ns"]),
            pid=int(raw_event["pid"]),
            tid=int(raw_event["tid"]),
            syscall=syscall,
            arguments_hash=self._args_hash(dict(raw_event.get("arguments", {}))),
            return_value=int(raw_event.get("return_value", 0)),
        )

    def _event_hash(self, event: CanonicalEvent) -> str:
        packed = json.dumps(
            {
                "sequence_number": event.sequence_number,
                "monotonic_timestamp_ns": event.monotonic_timestamp_ns,
                "pid": event.pid,
                "tid": event.tid,
                "syscall": event.syscall,
                "arguments_hash": event.arguments_hash,
                "return_value": event.return_value,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.blake2s(packed).hexdigest()

    def process_events(self, raw_events: list[dict[str, Any]]) -> dict[str, Any]:
        # Constant space per open fd: only the latest write-intent by (fd, offset).
        pending_write_intents: dict[tuple[int, int], CanonicalEvent] = {}
        emitted: list[CanonicalEvent] = []

        def flush_fd(fd: int) -> None:
            keys = [k for k in pending_write_intents if k[0] == fd]
            for key in keys:
                emitted.append(pending_write_intents.pop(key))

        for raw in raw_events:
            syscall = str(raw["syscall"])
            if syscall == "write":
                fd = int(raw.get("arguments", {}).get("fd", -1))
                offset = int(raw.get("arguments", {}).get("offset", 0))
                canonical = self.canonicalize(raw)
                if canonical is not None:
                    pending_write_intents[(fd, offset)] = canonical
                continue

            if syscall in {"close", "exit_group"}:
                fd = int(raw.get("arguments", {}).get("fd", -1))
                if fd >= 0:
                    flush_fd(fd)
                else:
                    for key in list(pending_write_intents):
                        emitted.append(pending_write_intents.pop(key))

            canonical = self.canonicalize(raw)
            if canonical is not None:
                emitted.append(canonical)

        for key in list(pending_write_intents):
            emitted.append(pending_write_intents.pop(key))

        emitted.sort(key=lambda e: e.sequence_number)
        for ev in emitted:
            self.mmr.append(self._event_hash(ev))

        return {
            "session_uuid": self.session_uuid,
            "captured_event_count": len(emitted),
            "mmr_root": self.mmr.finalize(),
            "events": [asdict(ev) for ev in emitted],
        }

    def run_file(self, input_trace_json: str, output_json: str) -> dict[str, Any]:
        started = time.time()
        try:
            raw_events = json.loads(Path(input_trace_json).read_text(encoding="utf-8"))
            if not isinstance(raw_events, list):
                raise ValueError("trace must be a list")
            result = self.process_events(raw_events)
            result["duration_seconds"] = round(time.time() - started, 6)
            Path(output_json).write_text(json.dumps(result, indent=2), encoding="utf-8")
            return result
        except Exception as exc:
            aborted = {
                "session_uuid": self.session_uuid,
                "status": "SessionAborted",
                "partial_mmr_root": self.mmr.finalize(),
                "reason": str(exc),
            }
            Path(output_json).write_text(json.dumps(aborted, indent=2), encoding="utf-8")
            raise CollectorAbort(str(exc)) from exc

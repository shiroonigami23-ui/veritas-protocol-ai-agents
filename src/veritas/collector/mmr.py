from __future__ import annotations

import hashlib
from dataclasses import dataclass


def _h(left: str, right: str) -> str:
    return hashlib.blake2s(f"{left}:{right}".encode("utf-8")).hexdigest()


@dataclass(slots=True)
class MMRProof:
    index: int
    leaf_hash: str
    siblings: list[str]


class MerkleMountainRange:
    """Minimal append-only MMR-like API for Iteration-1 integration tests."""

    def __init__(self) -> None:
        self._leaves: list[str] = []

    def append(self, event_hash: str) -> int:
        self._leaves.append(event_hash)
        return len(self._leaves) - 1

    def _build_tree_levels(self) -> list[list[str]]:
        if not self._leaves:
            return [[]]
        levels = [self._leaves[:]]
        while len(levels[-1]) > 1:
            src = levels[-1]
            nxt: list[str] = []
            for i in range(0, len(src), 2):
                left = src[i]
                right = src[i + 1] if i + 1 < len(src) else src[i]
                nxt.append(_h(left, right))
            levels.append(nxt)
        return levels

    def get_proof(self, index: int) -> MMRProof:
        if index < 0 or index >= len(self._leaves):
            raise IndexError("leaf index out of bounds")
        levels = self._build_tree_levels()
        siblings: list[str] = []
        pos = index
        for level in levels[:-1]:
            sib = pos ^ 1
            siblings.append(level[sib] if sib < len(level) else level[pos])
            pos //= 2
        return MMRProof(index=index, leaf_hash=self._leaves[index], siblings=siblings)

    def finalize(self) -> str:
        levels = self._build_tree_levels()
        if not levels[0]:
            return hashlib.blake2s(b"").hexdigest()
        return levels[-1][0]


import unittest
from veritas.core.pdl import PDLParseError, compile_policy_to_circuit, parse_policy

class TestPDL(unittest.TestCase):
    def test_parse_and_compile(self):
        rules = parse_policy('deny syscall.execve\nallow file.src/main.py\n')
        self.assertEqual(len(rules), 2)
        circuit = compile_policy_to_circuit(rules)
        self.assertIn('policy_root', circuit)

    def test_invalid_policy(self):
        with self.assertRaises(PDLParseError):
            parse_policy('block syscall.execve')

if __name__ == '__main__':
    unittest.main()

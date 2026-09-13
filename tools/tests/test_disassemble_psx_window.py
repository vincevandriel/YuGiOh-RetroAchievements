import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).parents[1] / "disassemble_psx_window.py"
SPEC = importlib.util.spec_from_file_location("disassemble_psx_window", MODULE_PATH)
assert SPEC and SPEC.loader
DISASM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISASM)


class PsxAddressTests(unittest.TestCase):
    def test_known_stock_cross_reference_offsets(self):
        self.assertEqual(DISASM.address_to_file_offset(0x80017AB0, 0x80010000), 0x82B0)
        self.assertEqual(DISASM.address_to_file_offset(0x80017AEC, 0x80010000), 0x82EC)

    def test_address_before_load_is_rejected(self):
        with self.assertRaises(ValueError):
            DISASM.address_to_file_offset(0x8000FFFF, 0x80010000)

    def test_address_parser_accepts_hex(self):
        self.assertEqual(DISASM.parse_address("0x80017AB0"), 0x80017AB0)


if __name__ == "__main__":
    unittest.main()

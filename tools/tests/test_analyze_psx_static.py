import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "analyze_psx_static.py"
SPEC = importlib.util.spec_from_file_location("analyze_psx_static", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class StaticAnalyzerContractTests(unittest.TestCase):
    def test_windows_are_bounded_and_word_aligned(self):
        for _, start, end in MODULE.WINDOWS:
            self.assertLessEqual(MODULE.CODE_START, start)
            self.assertLess(start, end)
            self.assertLessEqual(end, MODULE.CODE_END)
            self.assertEqual((start | end) & 3, 0)

    def test_scoped_regions_are_nonempty(self):
        for _, start, end in MODULE.SCOPED_REGIONS:
            self.assertLess(start, end)

    def test_sensitive_call_queries_are_present(self):
        for address in (0x800179F4, 0x80021810, 0x80021894, 0x8003F87C):
            self.assertIn(address, MODULE.QUERIES)


if __name__ == "__main__":
    unittest.main()

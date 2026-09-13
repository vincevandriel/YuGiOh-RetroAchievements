import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).parents[1] / "derive_record_layout.py"
SPEC = importlib.util.spec_from_file_location("derive_record_layout", MODULE_PATH)
assert SPEC and SPEC.loader
LAYOUT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAYOUT)


class LayoutMathTests(unittest.TestCase):
    def test_id_boundaries(self):
        self.assertEqual(LAYOUT.record_start_for_id(1), 0x00E9B000)
        self.assertEqual(LAYOUT.record_start_for_id(39), 0x00ED4000)
        with self.assertRaises(ValueError):
            LAYOUT.record_start_for_id(0)
        with self.assertRaises(ValueError):
            LAYOUT.record_start_for_id(40)

    def test_region_partition(self):
        cursor = 0
        for _, _, offset, size in LAYOUT.REGIONS[1:]:
            self.assertEqual(offset, cursor)
            cursor = offset + size
        self.assertEqual(cursor, LAYOUT.RECORD_SIZE)

    def test_array_geometry(self):
        self.assertEqual(LAYOUT.ARRAY_SIZE, 0x5A4)
        self.assertEqual(LAYOUT.ARRAY_STRIDE, 0x5B4)
        self.assertEqual(LAYOUT.ARRAY_STRIDE - LAYOUT.ARRAY_SIZE, 0x10)
        self.assertEqual([entry[2] for entry in LAYOUT.ARRAYS], [0, 0x5B4, 0xB68, 0x111C])

    def test_cpu_ra_boundaries(self):
        self.assertEqual(LAYOUT.cpu_to_ps1_ram(0x801781D8), 0x001781D8)
        self.assertEqual(LAYOUT.cpu_to_ps1_ram(0x801799D7), 0x001799D7)


if __name__ == "__main__":
    unittest.main()

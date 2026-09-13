#!/usr/bin/env python3
"""Fail-closed validator for the public Stage 2 evidence bundle."""

from __future__ import annotations

import csv
import json
from pathlib import Path


EXPECTED_ARRAY_OFFSETS = (0x0000, 0x05B4, 0x0B68, 0x111C)
EXPECTED_XREF = {
    0x80017A20: ("addiu", "$s0, $zero, 1"),
    0x80017AB4: ("lb", "$v0, -0x4c9f($v0)"),
    0x80017ABC: ("bltz", "$v0, 0x80017af0"),
    0x80017AC0: ("sllv", "$a2, $v0, $s0"),
    0x80017ACC: ("addu", "$a2, $a2, $v0"),
    0x80017AD0: ("addiu", "$a2, $a2, 0x1d33"),
    0x80017AD4: ("addiu", "$a3, $zero, 3"),
    0x80017AE8: ("jal", "0x80014e1c"),
    0x80017AEC: ("sw", "$v0, 0x18($sp)"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_hex(value: str) -> int:
    return int(value, 16)


def overlaps(a_start: int, a_size: int, b_start: int, b_end: int) -> bool:
    return a_size > 0 and a_start <= b_end and a_start + a_size - 1 >= b_start


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    evidence = root / "evidence" / "stage-02-disc-layout"

    layout = read_csv(evidence / "disc-layout.csv")
    assert len(layout) == 39
    for index, row in enumerate(layout, start=1):
        start = 0xE9B000 + 0x1800 * (index - 1)
        assert int(row["opponent_id"]) == index
        assert parse_hex(row["wa_record_start"]) == start
        assert parse_hex(row["wa_record_end_inclusive"]) == start + 0x17FF
        assert int(row["record_size"], 16) == 0x1800
        assert int(row["disc_lba_start"]) == 10102 + start // 0x800
        assert int(row["disc_lba_end_inclusive"]) == 10102 + start // 0x800 + 2
        for array_index, offset in enumerate(EXPECTED_ARRAY_OFFSETS):
            assert parse_hex(row[f"array_{array_index}_start"]) == start + offset

    arrays = read_csv(evidence / "array-statistics.csv")
    assert len(arrays) == 156
    nonzero_counts = []
    for row in arrays:
        assert int(row["size_bytes"]) == 1444
        assert int(row["element_width"]) == 2
        assert int(row["element_count"]) == 722
        assert int(row["sum"]) == 2048
        assert row["semantic_lead"].endswith("_lead")
        nonzero_counts.append(int(row["nonzero_count"]))
    assert min(nonzero_counts) == 13 and max(nonzero_counts) == 169

    address_map = read_csv(evidence / "address-map.csv")
    assert len(address_map) == 39 * 11
    for row in address_map:
        assert row["producer_routine"] == "UNRESOLVED_STAGE_3"
        assert row["consumer_routines"] == "UNRESOLVED_STAGE_3"
        assert any(marker in row["role"] for marker in ("lead", "unknown"))

    boundary = json.loads((evidence / "boundary-tests.json").read_text(encoding="utf-8"))
    assert boundary["translation"]["record_cpu_start"] == "0x801781D8"
    assert boundary["translation"]["record_ra_start"] == "0x1781D8"
    for region in boundary["regions"]:
        start = parse_hex(region["ra_start"])
        end = parse_hex(region["ra_end_inclusive"])
        assert end - start + 1 == int(region["size"])
        for vector in region["overlap_vectors"]:
            actual = overlaps(parse_hex(vector["read_start"]), int(vector["read_size"]), start, end)
            assert actual is vector["expected_overlap"]

    discovery = json.loads((evidence / "discovery.json").read_text(encoding="utf-8"))
    assert discovery["sector_aligned_records_with_four_arrays_summing_to_2048"] == 40
    assert discovery["consecutive_39_record_run_starts"] == ["0x00E99800", "0x00E9B000"]
    assert discovery["extra_predecessor_matches_opponent_record_ids"] == [1]
    assert discovery["signature_scan_uniquely_identifies_id_1"] is False

    xref_rows = read_csv(evidence / "stock-layout-xref.csv")
    assert len(xref_rows) == 57
    xref = {parse_hex(row["cpu_address"]): (row["mnemonic"], row["operands"]) for row in xref_rows}
    for address, expected in EXPECTED_XREF.items():
        assert xref[address] == expected

    facts = read_csv(evidence / "facts.csv")
    assert {row["fact_id"] for row in facts} == {
        "LAYOUT-001", "LAYOUT-002", "LAYOUT-003", "LAYOUT-004",
        "LAYOUT-005", "XREF-001", "SEM-001",
    }
    assert next(row for row in facts if row["fact_id"] == "SEM-001")["status"] == "LEAD"

    contradictions = read_csv(evidence / "contradictions.csv")
    assert len(contradictions) == 1
    assert contradictions[0]["contradiction_id"] == "CON-LAYOUT-001"
    assert contradictions[0]["status"] == "RESOLVED"

    print("Stage 2 public evidence: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

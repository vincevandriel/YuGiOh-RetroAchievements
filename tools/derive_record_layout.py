#!/usr/bin/env python3
"""Derive and verify Forbidden Memories opponent-record layout.

The input WA_MRG.MRG remains private. This tool emits only addresses, lengths,
aggregate statistics, and cryptographic digests. It never writes input bytes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
from pathlib import Path


SECTOR = 0x800
WA_LBA = 10102
DUELIST_SECTOR_BASE = 0x1D33
FIRST_ID = 1
LAST_ID = 39
RECORD_SIZE = 0x1800
CARD_COUNT = 722
ARRAY_SIZE = CARD_COUNT * 2
ARRAY_STRIDE = 0x5B4
RAM_BASE = 0x801781D8
EXPECTED_WA_SIZE = 37748736
EXPECTED_TOTAL = 2048

ARRAYS = (
    ("array_0", "deck_weights_lead", 0x0000),
    ("array_1", "sa_pow_weights_lead", 0x05B4),
    ("array_2", "bcd_weights_lead", 0x0B68),
    ("array_3", "sa_tec_weights_lead", 0x111C),
)

REGIONS = (
    ("record", "current_opponent_record_lead", 0x0000, 0x1800),
    ("array_0", "deck_weights_lead", 0x0000, 0x05A4),
    ("gap_0", "alignment_or_unknown", 0x05A4, 0x0010),
    ("array_1", "sa_pow_weights_lead", 0x05B4, 0x05A4),
    ("gap_1", "alignment_or_unknown", 0x0B58, 0x0010),
    ("array_2", "bcd_weights_lead", 0x0B68, 0x05A4),
    ("gap_2", "alignment_or_unknown", 0x110C, 0x0010),
    ("array_3", "sa_tec_weights_lead", 0x111C, 0x05A4),
    ("gap_3", "alignment_or_unknown", 0x16C0, 0x0010),
    ("rank_candidate", "rank_data_lead", 0x16D0, 0x00C8),
    ("tail", "unknown_tail", 0x1798, 0x0068),
)


def sha256(data: bytes | memoryview) -> str:
    return hashlib.sha256(data).hexdigest()


def record_start_for_id(opponent_id: int) -> int:
    if not FIRST_ID <= opponent_id <= LAST_ID:
        raise ValueError(f"opponent id out of range: {opponent_id}")
    return (DUELIST_SECTOR_BASE + 3 * opponent_id) * SECTOR


def cpu_to_ps1_ram(address: int) -> int:
    return address & 0x001FFFFF


def valid_weight_record(data: memoryview, start: int) -> bool:
    if start < 0 or start + RECORD_SIZE > len(data):
        return False
    for _, _, offset in ARRAYS:
        values = struct.unpack_from(f"<{CARD_COUNT}H", data, start + offset)
        if sum(values) != EXPECTED_TOTAL:
            return False
    return True


def discover_runs(data: memoryview) -> tuple[list[int], list[int]]:
    valid = []
    for start in range(0, len(data) - RECORD_SIZE + 1, SECTOR):
        if valid_weight_record(data, start):
            valid.append(start)

    valid_set = set(valid)
    run_starts = []
    run_span = (LAST_ID - FIRST_ID) * RECORD_SIZE
    for start in valid:
        if start + run_span + RECORD_SIZE > len(data):
            continue
        if all(start + index * RECORD_SIZE in valid_set for index in range(LAST_ID - FIRST_ID + 1)):
            run_starts.append(start)
    return valid, run_starts


def write_disc_layout(output: Path, data: memoryview) -> None:
    fields = [
        "opponent_id",
        "wa_record_start",
        "wa_record_end_inclusive",
        "record_size",
        "disc_lba_start",
        "disc_lba_end_inclusive",
        "record_sha256",
        "array_0_start",
        "array_1_start",
        "array_2_start",
        "array_3_start",
        "rank_candidate_start",
        "tail_start",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for opponent_id in range(FIRST_ID, LAST_ID + 1):
            start = record_start_for_id(opponent_id)
            end = start + RECORD_SIZE
            writer.writerow(
                {
                    "opponent_id": opponent_id,
                    "wa_record_start": f"0x{start:08X}",
                    "wa_record_end_inclusive": f"0x{end - 1:08X}",
                    "record_size": f"0x{RECORD_SIZE:X}",
                    "disc_lba_start": WA_LBA + start // SECTOR,
                    "disc_lba_end_inclusive": WA_LBA + (end - 1) // SECTOR,
                    "record_sha256": sha256(data[start:end]),
                    "array_0_start": f"0x{start + ARRAYS[0][2]:08X}",
                    "array_1_start": f"0x{start + ARRAYS[1][2]:08X}",
                    "array_2_start": f"0x{start + ARRAYS[2][2]:08X}",
                    "array_3_start": f"0x{start + ARRAYS[3][2]:08X}",
                    "rank_candidate_start": f"0x{start + 0x16D0:08X}",
                    "tail_start": f"0x{start + 0x1798:08X}",
                }
            )


def write_array_statistics(output: Path, data: memoryview) -> None:
    fields = [
        "opponent_id",
        "array_index",
        "semantic_lead",
        "wa_start",
        "wa_end_inclusive",
        "size_bytes",
        "element_width",
        "element_count",
        "sum",
        "nonzero_count",
        "first_nonzero_card_id",
        "last_nonzero_card_id",
        "sha256",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for opponent_id in range(FIRST_ID, LAST_ID + 1):
            record_start = record_start_for_id(opponent_id)
            for index, (_, semantic_lead, offset) in enumerate(ARRAYS):
                start = record_start + offset
                end = start + ARRAY_SIZE
                values = struct.unpack_from(f"<{CARD_COUNT}H", data, start)
                nonzero = [i + 1 for i, value in enumerate(values) if value]
                writer.writerow(
                    {
                        "opponent_id": opponent_id,
                        "array_index": index,
                        "semantic_lead": semantic_lead,
                        "wa_start": f"0x{start:08X}",
                        "wa_end_inclusive": f"0x{end - 1:08X}",
                        "size_bytes": ARRAY_SIZE,
                        "element_width": 2,
                        "element_count": CARD_COUNT,
                        "sum": sum(values),
                        "nonzero_count": len(nonzero),
                        "first_nonzero_card_id": nonzero[0] if nonzero else "",
                        "last_nonzero_card_id": nonzero[-1] if nonzero else "",
                        "sha256": sha256(data[start:end]),
                    }
                )


def write_address_map(output: Path) -> None:
    fields = [
        "symbol",
        "cpu_kseg0_start",
        "cpu_kseg0_end",
        "ps1_ram_start",
        "ps1_ram_end",
        "ra_start",
        "ra_end",
        "slus_file_start",
        "slus_file_end",
        "wa_user_start",
        "wa_user_end",
        "disc_lba_start",
        "disc_lba_end",
        "size_bytes",
        "element_width",
        "element_count",
        "stride_bytes",
        "role",
        "producer_routine",
        "consumer_routines",
        "evidence_ids",
        "confidence",
        "notes",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for opponent_id in range(FIRST_ID, LAST_ID + 1):
            record_start = record_start_for_id(opponent_id)
            for name, role, offset, size in REGIONS:
                cpu_start = RAM_BASE + offset
                cpu_end = cpu_start + size - 1
                wa_start = record_start + offset
                wa_end = wa_start + size - 1
                element_width = 2 if name.startswith("array_") else ""
                element_count = CARD_COUNT if name.startswith("array_") else ""
                writer.writerow(
                    {
                        "symbol": f"opponent_{opponent_id:02d}_{name}",
                        "cpu_kseg0_start": f"0x{cpu_start:08X}",
                        "cpu_kseg0_end": f"0x{cpu_end:08X}",
                        "ps1_ram_start": f"0x{cpu_to_ps1_ram(cpu_start):08X}",
                        "ps1_ram_end": f"0x{cpu_to_ps1_ram(cpu_end):08X}",
                        "ra_start": f"0x{cpu_to_ps1_ram(cpu_start):06X}",
                        "ra_end": f"0x{cpu_to_ps1_ram(cpu_end):06X}",
                        "slus_file_start": "",
                        "slus_file_end": "",
                        "wa_user_start": f"0x{wa_start:08X}",
                        "wa_user_end": f"0x{wa_end:08X}",
                        "disc_lba_start": WA_LBA + wa_start // SECTOR,
                        "disc_lba_end": WA_LBA + wa_end // SECTOR,
                        "size_bytes": size,
                        "element_width": element_width,
                        "element_count": element_count,
                        "stride_bytes": ARRAY_STRIDE if name.startswith("array_") else "",
                        "role": role,
                        "producer_routine": "UNRESOLVED_STAGE_3",
                        "consumer_routines": "UNRESOLVED_STAGE_3",
                        "evidence_ids": "LAYOUT-001;LAYOUT-002",
                        "confidence": "High-layout/Lead-semantics",
                        "notes": "SLUS file columns are blank because this is disc data loaded into RAM, not executable-backed static data.",
                    }
                )


def boundary_record(name: str, offset: int, size: int) -> dict[str, object]:
    start = RAM_BASE + offset
    end = start + size - 1
    return {
        "region": name,
        "size": size,
        "cpu_start": f"0x{start:08X}",
        "cpu_end_inclusive": f"0x{end:08X}",
        "ra_start": f"0x{cpu_to_ps1_ram(start):06X}",
        "ra_end_inclusive": f"0x{cpu_to_ps1_ram(end):06X}",
        "round_trip_start": f"0x{0x80000000 | cpu_to_ps1_ram(start):08X}",
        "round_trip_end": f"0x{0x80000000 | cpu_to_ps1_ram(end):08X}",
        "overlap_vectors": [
            {
                "read_start": f"0x{cpu_to_ps1_ram(start):06X}",
                "read_size": 1,
                "expected_overlap": True,
            },
            {
                "read_start": f"0x{cpu_to_ps1_ram(end):06X}",
                "read_size": 1,
                "expected_overlap": True,
            },
            {
                "read_start": f"0x{cpu_to_ps1_ram(start) - 2:06X}",
                "read_size": 4,
                "expected_overlap": True,
            },
            {
                "read_start": f"0x{cpu_to_ps1_ram(end) + 1:06X}",
                "read_size": 1,
                "expected_overlap": False,
            },
        ],
    }


def write_boundary_tests(output: Path) -> None:
    payload = {
        "schema_version": 1,
        "translation": {
            "cpu_to_ps1_ram": "address & 0x001FFFFF",
            "ra_for_main_ram": "RA equals PS1 physical RAM offset",
            "record_cpu_start": f"0x{RAM_BASE:08X}",
            "record_ra_start": f"0x{cpu_to_ps1_ram(RAM_BASE):06X}",
        },
        "regions": [boundary_record(name, offset, size) for name, _, offset, size in REGIONS],
    }
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_schema(output: Path) -> None:
    lines = [
        "flowchart LR",
        "  W[WA_MRG.MRG at LBA 10102] --> R[Opponent record: 0x1800 bytes / 3 sectors]",
        "  R --> A0[Array 0: +0x0000, 722 x u16]",
        "  R --> G0[Gap: +0x05A4, 0x10]",
        "  R --> A1[Array 1: +0x05B4, 722 x u16]",
        "  R --> G1[Gap: +0x0B58, 0x10]",
        "  R --> A2[Array 2: +0x0B68, 722 x u16]",
        "  R --> G2[Gap: +0x110C, 0x10]",
        "  R --> A3[Array 3: +0x111C, 722 x u16]",
        "  R --> G3[Gap: +0x16C0, 0x10]",
        "  R --> RK[Candidate rank data: +0x16D0, 0xC8]",
        "  R --> T[Unknown tail: +0x1798, 0x68]",
        "  R -. load destination lead .-> M[CPU 0x801781D8 / RA 0x1781D8]",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wa_mrg", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()

    raw = args.wa_mrg.read_bytes()
    if len(raw) != EXPECTED_WA_SIZE:
        raise SystemExit(f"unexpected WA_MRG size: {len(raw)}")
    actual_hash = sha256(raw)
    if actual_hash.lower() != args.expected_sha256.lower():
        raise SystemExit("WA_MRG SHA-256 mismatch")

    data = memoryview(raw)
    valid, runs = discover_runs(data)
    formula_start = record_start_for_id(FIRST_ID)
    historical_start = 0x00E9B000
    predecessor_start = formula_start - RECORD_SIZE
    expected_runs = [predecessor_start, formula_start]
    if runs != expected_runs:
        raise SystemExit(
            "expected the predecessor and ID-1 39-record windows at "
            f"{[hex(x) for x in expected_runs]}; got {[hex(x) for x in runs]}"
        )
    if formula_start != historical_start:
        raise SystemExit("formula and historical ID-1 offsets disagree")

    args.output_directory.mkdir(parents=True, exist_ok=True)
    write_disc_layout(args.output_directory / "disc-layout.csv", data)
    write_array_statistics(args.output_directory / "array-statistics.csv", data)
    write_address_map(args.output_directory / "address-map.csv")
    write_boundary_tests(args.output_directory / "boundary-tests.json")
    write_schema(args.output_directory / "schema.mmd")

    discovery = {
        "schema_version": 1,
        "input_size": len(raw),
        "input_sha256": actual_hash,
        "sector_aligned_records_with_four_arrays_summing_to_2048": len(valid),
        "valid_record_starts": [f"0x{value:08X}" for value in valid],
        "consecutive_39_record_run_starts": [f"0x{value:08X}" for value in runs],
        "extra_predecessor_record_start": f"0x{predecessor_start:08X}",
        "extra_predecessor_record_sha256": sha256(
            data[predecessor_start : predecessor_start + RECORD_SIZE]
        ),
        "extra_predecessor_array_sha256": [
            sha256(
                data[
                    predecessor_start + offset : predecessor_start + offset + ARRAY_SIZE
                ]
            )
            for _, _, offset in ARRAYS
        ],
        "extra_predecessor_matches_opponent_record_ids": [
            opponent_id
            for opponent_id in range(FIRST_ID, LAST_ID + 1)
            if data[predecessor_start : predecessor_start + RECORD_SIZE]
            == data[
                record_start_for_id(opponent_id) : record_start_for_id(opponent_id)
                + RECORD_SIZE
            ]
        ],
        "formula_id_1_start": f"0x{formula_start:08X}",
        "historical_tool_id_1_start": f"0x{historical_start:08X}",
        "formula_and_historical_id_1_start_agree": True,
        "signature_scan_contains_formula_window": formula_start in runs,
        "signature_scan_uniquely_identifies_id_1": False,
        "semantic_warning": "The scan finds a valid predecessor record and cannot label ID 1 by byte pattern alone. Array roles and the predecessor's purpose remain leads until stock executable producers/consumers are proven in Stages 3 and 4.",
    }
    (args.output_directory / "discovery.json").write_text(
        json.dumps(discovery, indent=2) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "result": "PASS_WITH_RECORDED_AMBIGUITY",
                "valid_records": len(valid),
                "run_starts": [f"0x{value:08X}" for value in runs],
                "selected_id_1_start": f"0x{formula_start:08X}",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

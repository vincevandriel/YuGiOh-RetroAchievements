#!/usr/bin/env python3
"""Fail-closed validator for the public Stage 3 evidence bundle."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


EXPECTED_HASH = "84a54ed74f3d0edd6d81380839f7e4ef5bfb21ecea18be9a062bd6bfa5a45c88"
EXPECTED_CALLS = {
    "0x800179F4": ["0x8002D014"],
    "0x80021558": [
        "0x80021660", "0x80021680", "0x800216B8", "0x800216F0",
        "0x8002171C", "0x8002173C", "0x8002175C", "0x80021788",
        "0x800217A8", "0x800217C8",
    ],
    "0x80021598": ["0x80021A2C"],
    "0x80021810": ["0x80021C60"],
    "0x80021894": ["0x80021F14"],
    "0x800243F4": ["0x800245C0", "0x800245D0"],
    "0x800245A0": ["0x80017D94"],
    "0x80024DC8": ["0x8002DD3C", "0x80030F68"],
    "0x8003F87C": ["0x8002DAE8", "0x8002F3B0"],
    "0x8007E3D0": ["0x80013CCC", "0x80013DF8", "0x80013F60", "0x8007CFEC", "0x8007DEC8"],
    "0x8007E3F0": ["0x8007E3D8"],
}
EXPECTED_INSTRUCTIONS = {
    "0x80013CCC": ("jal", "0x8007e3d0"),
    "0x80013CD0": ("addiu", "$a1, $zero, 0x200"),
    "0x80013D1C": ("addiu", "$v0, $v0, 0x800"),
    "0x80013D38": ("addiu", "$a0, $a0, -0x800"),
    "0x80014A14": ("addiu", "$a2, $zero, 6"),
    "0x80014A1C": ("jal", "0x8007b468"),
    "0x80014B08": ("jal", "0x8001455c"),
    "0x80017AD0": ("addiu", "$a2, $a2, 0x1d33"),
    "0x80017AE8": ("jal", "0x80014e1c"),
    "0x80021848": ("andi", "$v0, $v0, 0x7ff"),
    "0x80021874": ("slti", "$v0, $v1, 0x2d2"),
    "0x80021C60": ("jal", "0x80021810"),
    "0x80021C78": ("sh", "$v0, 0x3c($a0)"),
    "0x80021F14": ("jal", "0x80021894"),
    "0x8002444C": ("addiu", "$s7, $v0, -0x7e28"),
    "0x800244CC": ("slti", "$v0, $s1, 0x2d0"),
    "0x800244D8": ("slti", "$v0, $s3, 0x28"),
    "0x80024DF0": ("sb", "$a1, -0x4c9f($at)"),
    "0x8003856C": ("sb", "$a1, -0x4c9f($at)"),
    "0x8003F89C": ("jal", "0x800356a0"),
    "0x8003F8A0": ("addiu", "$a2, $zero, 0x680"),
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    stage = root / "evidence" / "stage-03-static-re"
    required = {
        "README.md", "stage-report.md", "facts.csv", "contradictions.csv",
        "reproduction.md", "artifacts.sha256", "executable-map.json",
        "functions.csv", "load-callgraph.mmd", "interpret-callgraph.mmd",
        "award-callgraph.mmd", "instruction-evidence.md",
        "instruction-windows.csv", "direct-call-xrefs.csv", "pointer-xrefs.csv",
        "constant-hits.csv", "effective-address-candidates.csv",
        "record-request-contexts.csv",
        "range-writers.csv", "range-readers.csv", "native-validation-search.csv",
    }
    assert required == {path.name for path in stage.iterdir() if path.is_file()}

    mapping = json.loads((stage / "executable-map.json").read_text(encoding="utf-8"))
    assert mapping["input_sha256"] == EXPECTED_HASH
    assert mapping["load_address"] == "0x80010000"
    assert mapping["analysis_start"] == "0x80012800"
    assert mapping["analysis_end_exclusive"] == "0x800906E0"
    assert mapping["private_path_recorded"] is False

    calls = rows(stage / "direct-call-xrefs.csv")
    by_target: dict[str, list[str]] = {}
    for row in calls:
        by_target.setdefault(row["target"], []).append(row["call_site"])
    for target, sites in EXPECTED_CALLS.items():
        assert by_target[target] == sites

    pointers = rows(stage / "pointer-xrefs.csv")
    assert [(r["target"], r["file_offset"]) for r in pointers] == [
        ("0x80020F4C", "0x000811C8"),
        ("0x80024E58", "0x00081268"),
        ("0x800218F0", "0x000811CC"),
        ("0x80038530", "0x000816E0"),
    ]
    request_contexts = rows(stage / "record-request-contexts.csv")
    assert len({row["call_site"] for row in request_contexts}) == 21

    instructions = rows(stage / "instruction-windows.csv")
    assert len(instructions) == 1225
    assert all(row["input_sha256"] == EXPECTED_HASH for row in instructions)
    decoded = {row["cpu_address"]: (row["mnemonic"], row["operands"]) for row in instructions}
    for address, expected in EXPECTED_INSTRUCTIONS.items():
        assert decoded[address] == expected

    functions = rows(stage / "functions.csv")
    assert len(functions) == 24
    assert {row["function_id"] for row in functions} == {f"FN-{i:03d}" for i in range(1, 25)}

    readers = rows(stage / "range-readers.csv")
    assert {row["reader_id"] for row in readers} == {f"READ-{i:03d}" for i in range(1, 10)}
    assert {row["reader_id"] for row in readers if row["classification"] == "consumer"} == {
        "READ-001", "READ-002", "READ-003", "READ-004", "READ-005"
    }
    writers = rows(stage / "range-writers.csv")
    assert len(writers) == 5 and writers[0]["writer_id"] == "WRITE-001"
    assert writers[1]["classification"] == "false-positive"

    validations = rows(stage / "native-validation-search.csv")
    assert len(validations) == 9
    assert all(row["result"] for row in validations)

    facts = rows(stage / "facts.csv")
    assert len(facts) == 16
    assert all(row["status"] in {"CONFIRMED", "CORROBORATED"} for row in facts)
    negatives = [row for row in facts if row["fact_id"] in {"STATIC-RANGE-001", "STATIC-VALID-001"}]
    assert all(row["confidence"] == "Medium" for row in negatives)

    contradictions = rows(stage / "contradictions.csv")
    assert len(contradictions) == 2
    assert all(row["status"] == "RESOLVED" for row in contradictions)

    for graph in ("load-callgraph.mmd", "interpret-callgraph.mmd", "award-callgraph.mmd"):
        text = (stage / graph).read_text(encoding="utf-8")
        assert text.startswith("flowchart TD\n") and "0x" in text

    report = (stage / "stage-report.md").read_text(encoding="utf-8")
    assert "Result: `PASS`" in report
    assert "Stage 4" in report and "not started" in report

    manifest_rows = (stage / "artifacts.sha256").read_text(encoding="utf-8").splitlines()
    expected_names = sorted(required - {"artifacts.sha256"})
    actual_names = []
    for line in manifest_rows:
        digest, name = line.split("  ", 1)
        actual_names.append(name)
        assert hashlib.sha256((stage / name).read_bytes()).hexdigest() == digest
    assert sorted(actual_names) == expected_names
    print("Stage 3 public evidence: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

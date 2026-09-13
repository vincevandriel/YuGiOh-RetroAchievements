#!/usr/bin/env python3
"""Emit a narrow, reproducible MIPS disassembly window from a PS-X EXE.

The executable remains private. Output is limited to instruction-sized evidence
inside an explicitly requested address range and contains no input path.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import struct
from pathlib import Path


PSX_HEADER_SIZE = 0x800


def parse_u32_le(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def address_to_file_offset(address: int, load_address: int) -> int:
    if address < load_address:
        raise ValueError("address precedes executable load address")
    return PSX_HEADER_SIZE + address - load_address


def parse_address(value: str) -> int:
    return int(value, 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--start", type=parse_address, required=True)
    parser.add_argument("--end", type=parse_address, required=True,
                        help="exclusive CPU address")
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()

    data = args.executable.read_bytes()
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if actual_sha256.lower() != args.expected_sha256.lower():
        raise SystemExit("executable SHA-256 mismatch")
    if data[:8] != b"PS-X EXE":
        raise SystemExit("input is not a PS-X EXE")

    load_address = parse_u32_le(data, 0x18)
    text_size = parse_u32_le(data, 0x1C)
    if len(data) != PSX_HEADER_SIZE + text_size:
        raise SystemExit("PS-X EXE file size does not match declared text size")
    if args.start % 4 or args.end % 4 or args.end <= args.start:
        raise SystemExit("address window must be non-empty and word-aligned")

    start_offset = address_to_file_offset(args.start, load_address)
    end_offset = address_to_file_offset(args.end, load_address)
    if start_offset < PSX_HEADER_SIZE or end_offset > len(data):
        raise SystemExit("address window is outside the executable text extent")

    try:
        from capstone import Cs, CS_ARCH_MIPS, CS_MODE_LITTLE_ENDIAN, CS_MODE_MIPS32
        import capstone
    except ImportError as exc:
        raise SystemExit("capstone is required: python -m pip install capstone==5.0.6") from exc

    decoder = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
    instructions = list(decoder.disasm(data[start_offset:end_offset], args.start))
    expected_count = (args.end - args.start) // 4
    if len(instructions) != expected_count:
        raise SystemExit(f"decoded {len(instructions)} instructions; expected {expected_count}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow([
            "cpu_address", "file_offset", "instruction_bytes_le",
            "mnemonic", "operands", "tool", "input_sha256",
        ])
        for insn in instructions:
            writer.writerow([
                f"0x{insn.address:08X}",
                f"0x{address_to_file_offset(insn.address, load_address):08X}",
                insn.bytes.hex(),
                insn.mnemonic,
                insn.op_str,
                f"capstone-{capstone.__version__}",
                actual_sha256,
            ])

    print(f"wrote {len(instructions)} instructions; input verified; path withheld")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

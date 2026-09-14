#!/usr/bin/env python3
"""Create bounded, reproducible static-xref evidence from the exact PS-X EXE.

The executable remains private. The tool emits only compact aggregate/xref rows
and narrow allowlisted disassembly windows; it never records the input path.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import struct
from pathlib import Path


HEADER = 0x800
CODE_START = 0x80012800
CODE_END = 0x800906E0
QUERIES = {
    0x800137E4: "io_wait_pump",
    0x80013940: "request_geometry",
    0x80013998: "request_descriptor",
    0x80013C28: "sector_ready_callback",
    0x800140A0: "packet_callback",
    0x8001455C: "disc_state_machine",
    0x80014A5C: "disc_scheduler_tick",
    0x80014E1C: "record_request_wrapper",
    0x800179F4: "duel_asset_loader",
    0x80020F4C: "duel_ui_auxiliary_record_loader",
    0x80021558: "rank_threshold_lookup",
    0x80021598: "rank_score_builder",
    0x80021810: "weighted_reward_roll",
    0x80021894: "inventory_and_history_update",
    0x800218F0: "duel_result_state",
    0x800243F4: "deck_builder",
    0x800245A0: "two_side_deck_setup",
    0x80024E58: "generic_indexed_asset_loader",
    0x80024DC8: "duel_global_setup",
    0x8002CEE8: "duel_state_machine",
    0x80038530: "script_duel_setup",
    0x8003F87C: "save_image_copy_and_write",
    0x8007B468: "psyq_DsPacket",
    0x8007E3D0: "CD_getsector_wrapper",
    0x8007E3F0: "psyq_CD_getsector",
}
POINTER_QUERIES = {
    0x80020F4C: "duel_ui_auxiliary_record_loader",
    0x80024E58: "generic_indexed_asset_loader",
    0x80021810: "weighted_reward_roll",
    0x80021894: "inventory_and_history_update",
    0x800218F0: "duel_result_state",
    0x80038530: "script_duel_setup",
}
IMMEDIATES = {0x02D2, 0x05A4, 0x05B4, 0x0800, 0x1800, 0x1D33, 0x07FF}
IMMEDIATE_MNEMONICS = {"addi", "addiu", "andi", "ori", "slti", "sltiu"}
WINDOWS = [
    ("request_geometry", 0x80013940, 0x80013A94),
    ("sector_copy", 0x80013C28, 0x80013D54),
    ("packet_callback", 0x800140A0, 0x80014134),
    ("disc_initiation", 0x800148E8, 0x80014A28),
    ("scheduler_bridge", 0x80014A5C, 0x80014B30),
    ("record_request", 0x80014E1C, 0x80014EEC),
    ("record_callsite", 0x80017AB0, 0x80017AF4),
    ("object_pool_allocation", 0x80017BE0, 0x80017C54),
    ("auxiliary_record_request", 0x800210E0, 0x8002112C),
    ("rank_lookup", 0x80021558, 0x80021598),
    ("rank_consumers", 0x80021638, 0x800217EC),
    ("weighted_roll", 0x80021810, 0x80021894),
    ("inventory_award", 0x80021894, 0x800218F0),
    ("tier_decision", 0x800219F0, 0x80021AA4),
    ("roll_storage", 0x80021C00, 0x80021C8C),
    ("award_call", 0x80021EF0, 0x80021F24),
    ("deck_consumer", 0x800243F4, 0x800245A0),
    ("adjacent_false_positive", 0x80024734, 0x80024914),
    ("duel_setup", 0x80024DC8, 0x80024E28),
    ("duel_loader_ancestor", 0x8002CF10, 0x8002D02C),
    ("script_opponent_writer", 0x80038530, 0x80038690),
    ("result_card_reader", 0x80037DF0, 0x80037F10),
    ("save_copy", 0x8003F87C, 0x8003F8D4),
]
SCOPED_REGIONS = [
    ("resident_record", 0x801781D8, 0x801799D8),
]
MEMORY_RE = re.compile(r"(?:(-?0x[0-9a-f]+|-?[0-9]+))?\(\$(\w+)\)$")


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def file_offset(address: int, load: int) -> int:
    return HEADER + address - load


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()

    data = args.executable.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest.lower() != args.expected_sha256.lower():
        raise SystemExit("executable SHA-256 mismatch")
    if data[:8] != b"PS-X EXE":
        raise SystemExit("input is not a PS-X EXE")
    load, size, entry, gp = u32(data, 0x18), u32(data, 0x1C), u32(data, 0x10), u32(data, 0x14)
    if len(data) != HEADER + size:
        raise SystemExit("file size does not match PS-X EXE header")
    if not (load <= CODE_START < CODE_END <= load + size):
        raise SystemExit("declared static-analysis range is outside executable")

    try:
        import capstone
        from capstone import Cs, CS_ARCH_MIPS, CS_MODE_LITTLE_ENDIAN, CS_MODE_MIPS32
    except ImportError as exc:
        raise SystemExit("capstone==5.0.6 is required") from exc

    decoder = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
    decoder.skipdata = True
    start_off, end_off = file_offset(CODE_START, load), file_offset(CODE_END, load)
    insns = list(decoder.disasm(data[start_off:end_off], CODE_START))

    calls: list[dict[str, object]] = []
    constants: list[dict[str, object]] = []
    for insn in insns:
        if insn.mnemonic == "jal":
            try:
                target = int(insn.op_str, 16)
            except ValueError:
                continue
            if target in QUERIES:
                calls.append({
                    "target": f"0x{target:08X}", "target_role": QUERIES[target],
                    "call_site": f"0x{insn.address:08X}",
                    "file_offset": f"0x{file_offset(insn.address, load):08X}",
                    "instruction_bytes_le": insn.bytes.hex(),
                })
        parts = [part.strip() for part in insn.op_str.split(",")]
        for part in (parts[-1:] if insn.mnemonic in IMMEDIATE_MNEMONICS else []):
            try:
                value = int(part, 0) & 0xFFFF
            except ValueError:
                continue
            if value in IMMEDIATES:
                constants.append({
                    "value": f"0x{value:04X}", "cpu_address": f"0x{insn.address:08X}",
                    "mnemonic": insn.mnemonic, "operands": insn.op_str,
                    "disposition": "grouped-in-native-validation-search.csv",
                })
                break

    pointers: list[dict[str, object]] = []
    for target, role in POINTER_QUERIES.items():
        needle = struct.pack("<I", target)
        cursor = 0
        while True:
            hit = data.find(needle, cursor)
            if hit < 0:
                break
            pointers.append({
                "target": f"0x{target:08X}", "target_role": role,
                "file_offset": f"0x{hit:08X}",
                "mapped_cpu_address": f"0x{load + hit - HEADER:08X}" if hit >= HEADER else "PSX_HEADER",
            })
            cursor = hit + 1

    # Lightweight constant propagation recovers direct effective addresses.
    # Rows are candidates for manual disposition, not a whole-program alias proof.
    regs: dict[str, tuple[int, int]] = {"gp": (gp, CODE_START)}
    memory_refs: list[dict[str, object]] = []
    load_ops = {"lb", "lbu", "lh", "lhu", "lw", "lwl", "lwr"}
    store_ops = {"sb", "sh", "sw", "swl", "swr"}
    volatile = {"v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3",
                "t4", "t5", "t6", "t7", "t8", "t9", "at"}
    for insn in insns:
        operands = [part.strip() for part in insn.op_str.split(",")]
        mnemonic = insn.mnemonic
        if mnemonic in load_ops | store_ops and len(operands) >= 2:
            match = MEMORY_RE.search(operands[-1])
            if match and match.group(2) in regs:
                offset = int(match.group(1) or "0", 0)
                base, origin = regs[match.group(2)]
                address = (base + offset) & 0xFFFFFFFF
                for region, lo, hi in SCOPED_REGIONS:
                    if lo <= address < hi:
                        memory_refs.append({
                            "region": region, "effective_address": f"0x{address:08X}",
                            "access": "read" if mnemonic in load_ops else "write",
                            "width": {"lb": 1, "lbu": 1, "sb": 1, "lh": 2, "lhu": 2,
                                      "sh": 2, "lw": 4, "lwl": 4, "lwr": 4,
                                      "sw": 4, "swl": 4, "swr": 4}[mnemonic],
                            "cpu_address": f"0x{insn.address:08X}",
                            "mnemonic": mnemonic, "operands": insn.op_str,
                            "constant_origin": f"0x{origin:08X}",
                            "disposition": "range-readers-or-range-writers.csv",
                        })
        if mnemonic == "lui" and len(operands) == 2:
            regs[operands[0].lstrip("$")] = (int(operands[1], 0) << 16, insn.address)
        elif mnemonic in {"addiu", "addi", "ori"} and len(operands) == 3:
            dst, src = operands[0].lstrip("$"), operands[1].lstrip("$")
            if src in regs:
                base, origin = regs[src]
                immediate = int(operands[2], 0)
                regs[dst] = ((base + immediate) & 0xFFFFFFFF if mnemonic != "ori"
                             else base | (immediate & 0xFFFF), origin)
            else:
                regs.pop(dst, None)
        elif mnemonic == "move" and len(operands) == 2:
            dst, src = operands[0].lstrip("$"), operands[1].lstrip("$")
            if src in regs:
                regs[dst] = regs[src]
            else:
                regs.pop(dst, None)
        elif mnemonic in load_ops and operands:
            regs.pop(operands[0].lstrip("$"), None)
        elif mnemonic in {"jal", "jalr"}:
            for register in volatile:
                regs.pop(register, None)

    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "format": "PS-X EXE", "input_sha256": digest, "entry": f"0x{entry:08X}",
        "initial_gp": f"0x{gp:08X}", "load_address": f"0x{load:08X}",
        "declared_text_size": size, "file_size": len(data),
        "analysis_start": f"0x{CODE_START:08X}", "analysis_end_exclusive": f"0x{CODE_END:08X}",
        "analyzed_bytes": CODE_END - CODE_START, "decoder": f"capstone-{capstone.__version__}",
        "private_path_recorded": False,
    }
    (args.output / "executable-map.json").write_bytes((json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
    write_csv(args.output / "direct-call-xrefs.csv", list(calls[0]) if calls else [], calls)
    write_csv(args.output / "pointer-xrefs.csv", list(pointers[0]) if pointers else [], pointers)
    write_csv(args.output / "constant-hits.csv", list(constants[0]) if constants else [], constants)
    write_csv(args.output / "effective-address-candidates.csv",
              list(memory_refs[0]) if memory_refs else [], memory_refs)
    request_context: list[dict[str, object]] = []
    for index, insn in enumerate(insns):
        if insn.mnemonic == "jal" and insn.op_str == "0x80014e1c":
            for nearby in insns[max(0, index - 14):index + 2]:
                request_context.append({
                    "call_site": f"0x{insn.address:08X}",
                    "cpu_address": f"0x{nearby.address:08X}",
                    "mnemonic": nearby.mnemonic, "operands": nearby.op_str,
                    "instruction_bytes_le": nearby.bytes.hex(),
                })
    write_csv(args.output / "record-request-contexts.csv",
              list(request_context[0]) if request_context else [], request_context)

    rows: list[dict[str, object]] = []
    for label, start, end in WINDOWS:
        chunk = data[file_offset(start, load):file_offset(end, load)]
        decoded = list(decoder.disasm(chunk, start))
        if len(decoded) != (end - start) // 4:
            raise SystemExit(f"window {label} did not decode completely")
        for insn in decoded:
            rows.append({
                "window": label, "cpu_address": f"0x{insn.address:08X}",
                "file_offset": f"0x{file_offset(insn.address, load):08X}",
                "instruction_bytes_le": insn.bytes.hex(), "mnemonic": insn.mnemonic,
                "operands": insn.op_str, "input_sha256": digest,
            })
    write_csv(args.output / "instruction-windows.csv", list(rows[0]), rows)
    print(json.dumps({"status": "PASS", "calls": len(calls), "pointers": len(pointers),
                      "constant_hits": len(constants), "window_instructions": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

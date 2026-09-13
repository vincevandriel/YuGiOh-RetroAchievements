# Stage 2 reproduction

Private input paths must be supplied locally and must not be committed or echoed.

## STAGE2-REPRO-001 — Derive all record and subregion boundaries

Run `tools/derive_record_layout.py` against the accepted private `WA_MRG.MRG`,
requiring size `37748736` and SHA-256
`2026d85d3f224e04afc74e6fde70938195048883192fe845ffcadb8b286cc3f4`.
Write results to `evidence/stage-02-disc-layout`. Require 39 selected rows,
ID 1 start `0xE9B000`, ID 39 start `0xED4000`, record size `0x1800`, and no
out-of-bounds region.

Independently inspect the pinned FMScrambler implementation at lines 425–490.
Require its 39-entry formula and all four array offsets to match every generated
boundary. Do not use its semantic variable names as proof of game behavior.

## STAGE2-REPRO-002 — Reconcile array statistics

Parse all four candidate arrays per selected record as 722 little-endian `u16`
values. Require 156 rows, size 1444, element count 722, and sum 2048 for every
row. Require nonzero-count extrema 13 and 169. Publish no array values.

## STAGE2-REPRO-003 — Repeat the structural discovery scan

Scan every 2048-byte-aligned `0x1800`-byte window in the accepted file. A valid
candidate has four arrays at the generated offsets, each summing to 2048.
Require 40 valid starts and two consecutive 39-record windows beginning at
`0xE99800` and `0xE9B000`. Hash the predecessor and all four arrays; require an
exact digest match to selected opponent ID 1. Record, rather than suppress, the
non-unique signature result.

## STAGE2-REPRO-004 — Verify address translations and overlap vectors

Starting with CPU KSEG0 destination `0x801781D8`, independently apply
`address & 0x001FFFFF`. Require result `0x1781D8` and inclusive record end
`0x1799D7`. Compare the range with the pinned rcheevos PlayStation map in
`consoleinfo.c` lines 805–812. For each generated region, execute the four
stored overlap vectors and require their calculated results to equal
`expected_overlap`. `tools/validate_stage2.py` performs these checks against the
public bundle.

## STAGE2-REPRO-005 — Recreate the exact stock call-site evidence

Install Capstone 5.0.6. Run `tools/disassemble_psx_window.py` against the
accepted private `SLUS_014.11`, addresses `0x80017A10` through exclusive
`0x80017AF4`, requiring SHA-256
`84a54ed74f3d0edd6d81380839f7e4ef5bfb21ecea18be9a062bd6bfa5a45c88`.

Require:

- CPU `0x80017A20`: `$s0 = 1`;
- `0x80017AB4`: signed byte load using base `0x800A0000` and offset `-0x4C9F`;
- `0x80017ABC`: negative-value branch around the call;
- `0x80017AC0–0x80017AD0`: `2 * value + value + 0x1D33` in `$a2`;
- `0x80017AD4`: `$a3 = 3`;
- `0x80017AD8–0x80017ADC`: construction of `0x801781D8`;
- `0x80017AE8`: call target `0x80014E1C`;
- `0x80017AEC`: destination stored in the seventh argument slot.

The tool verifies the PS-X EXE marker, load address, declared text extent, total
size, and digest before emitting a narrow instruction window. It does not emit
the private input path.

## STAGE2-REPRO-006 — Enforce semantic status

Inspect `address-map.csv` and `facts.csv`. Require all deck/reward/rank names to
contain `lead`, `candidate`, or `unknown`; producer and consumer fields must be
`UNRESOLVED_STAGE_3`; and the stage confidence statement must cap semantics at
Medium pending Stages 3–4.

## STAGE2-REPRO-007 — Gate integrity

Run `tools/validate_stage2.py` and all unit tests, parse every JSON and CSV,
recompute `artifacts.sha256`, run
the Stage 0 prohibited-file and credential scans, and run Git whitespace
validation. Any mismatch, private path, proprietary input, unresolved boundary
error, or semantic overclaim fails the gate.

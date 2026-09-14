# Stage 3 reproduction

All procedures are read-only with respect to the accepted private executable.
Substitute a local path for `<SLUS>`; the path is never written to evidence.

## STAGE3-REPRO-001 — deterministic static scan

```powershell
python tools/analyze_psx_static.py <SLUS> evidence/stage-03-static-re `
  --expected-sha256 84a54ed74f3d0edd6d81380839f7e4ef5bfb21ecea18be9a062bd6bfa5a45c88
```

Expected final JSON starts with `{"status":"PASS"` (spacing may differ), the
input hash is accepted, and no private path appears in an artifact.

The analyzer parses the PS-X EXE header, disassembles only the declared mapped
range for aggregate scans, searches the full file for four exact function
pointers, and emits only compact xrefs plus allowlisted instruction windows.

## STAGE3-REPRO-002 — instruction data-flow review

1. Filter `instruction-windows.csv` by the window names documented in
   `instruction-evidence.md`.
2. Recalculate each address from `SLUS-FILE = CPU - 0x80010000 + 0x800`.
3. Follow register and stack arguments through the load graph.
4. For the deck and reward loops, independently evaluate the shift/add
   sequences and confirm target range, element width, comparison, loop bound,
   and returned numbering.
5. Confirm every graph edge names its exact `jal`, indirect dispatch entry, or
   global producer/consumer address.

## STAGE3-REPRO-003 — Psy-Q identification

1. At pinned matching-decomp revision
   `18bcb5806cb3dff60d3d3ee7163ce55ff6884c00`, inspect
   `config/symbol_addrs.txt` for `DsPacket=0x8007B468` and
   `CD_getsector=0x8007E3F0`.
2. In `instruction-windows.csv`, verify the call and arguments at
   `0x80014A08–0x80014A24` and the wrapper call at `0x80013CC8–0x80013CD0`.
3. Compare command and retry semantics with the original Psy-Q
   [Library Overview](https://psx.arthus.net/sdk/Psy-Q/DOCS/Devrefs/Libovr.pdf).

## STAGE3-REPRO-004 — negative-search disposition

1. Reconcile all `0x02D2`, `0x05A4`, `0x05B4`, `0x0800`, `0x1800`,
   `0x1D33`, and `0x07FF` hits in `constant-hits.csv` against
   `native-validation-search.csv`.
2. Reconcile every scoped candidate in `effective-address-candidates.csv`
   against `range-readers.csv`, `range-writers.csv`, and the contradiction
   ledger.
3. Confirm that no open contradiction remains and that static negative claims
   are capped at Medium pending runtime corroboration.

## STAGE3-REPRO-005 — public gate

```powershell
python tools/validate_stage3.py
python -m unittest discover -s tools/tests -p "test_*.py"
git diff --check
```

Expected: Stage 3 `PASS`, all tests pass, and the whitespace check is silent.

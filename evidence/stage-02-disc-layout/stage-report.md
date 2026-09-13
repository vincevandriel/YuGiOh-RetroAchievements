# Stage 2 — WA_MRG disc schema and RAM layout

## Gate

- Result: `PASS`
- Executor: Codex, highest available reasoning
- Started UTC: 2026-09-13T21:42:47Z
- Completed UTC: 2026-09-13T21:52:29Z
- Stage 1 gate revision: `ea959435a743c1ec75b2926487fc6dc5c6a2b630`

## Outcome

Two independent address derivations agree on every selected opponent-record
boundary: the exact stock executable computes WA sector `0x1D33 + 3 * value`
and the historical direct-offset implementation selects
`0xE9B000 + 0x1800 * index` for 39 records. The accepted private data validates
all predicted boundaries and subregions.

All 156 candidate arrays are exactly 722 little-endian words, remain inside the
accepted file, and sum to 2048. The full selected record window spans
WA-relative `0xE9B000–0xED57FF`, absolute disc LBAs 17580–17696. The exact
stock caller supplies candidate RAM destination `0x801781D8`, yielding record
range `0x801781D8–0x801799D7` and RA range `0x1781D8–0x1799D7`.

The discovery scan produced an important correction: there is a fortieth valid
predecessor record at `0xE99800`, byte-for-byte identical to selected ID 1.
This creates two valid 39-record signature windows. It is recorded as a resolved
contradiction because the exact stock sector formula and historical direct
offset independently select `0xE9B000`; the predecessor's purpose remains
unknown and signature-only ID labelling is disallowed.

## Evidence-level boundary

High confidence applies to byte geometry, selected addresses, aggregate
statistics, exact stock instruction evidence, and CPU/RA conversion. Semantic
confidence is capped at Medium: “deck,” reward tiers, rank block, and unused
tail are still leads. Stage 3 must recover `0x80014E1C` and the producer/call
graph; Stage 4 must recover array consumers and the award path.

## Safety and privacy check

- Private executable and disc data were read only: yes.
- Only narrow instruction evidence, addresses, statistics, and digests were
  published: yes.
- Raw tables, disc files, private paths, and credentials were excluded: yes.
- No emulator session or RetroAchievements session was started: yes.
- No file modification, bypass, concealment, or altered-target experiment was
  performed: yes.

## Gate checklist

- [x] Two independent derivations agree on every selected record boundary.
- [x] All 39 records and 156 arrays remain in bounds and reconcile.
- [x] Raw/user sector arithmetic is explicit and unambiguous.
- [x] CPU, physical RAM, and RA coordinates pass boundary tests.
- [x] The unexpected predecessor is preserved in the contradiction ledger.
- [x] Every semantic label retains lead/candidate/unknown status.
- [x] Unit tests, structured-artifact parsing, hashes, scans, and whitespace
  checks pass.
- [x] No private or copyrighted source data is committed.

## Sources

1. Exact accepted stock executable, narrow evidence in `stock-layout-xref.csv`.
2. FMScrambler,
   [`DataScrambler.cs` at `94d4429`](https://github.com/forbidden-memories-coding/fmscrambler/blob/94d44292cfd51aa24a29b2a42131413e5f25aff2/FMLib/Randomizer/DataScrambler.cs#L425-L490).
3. YuGiOhForbiddenMemoriesRecomp,
   [`psx_cpu_data.c` at `6b3579c`](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_cpu_data.c#L3-L22).
4. rcheevos,
   [`consoleinfo.c` at `c28462e`](https://github.com/RetroAchievements/rcheevos/blob/c28462eafdbeb881a1d442754dd17aae5c4ab834/src/rcheevos/consoleinfo.c#L805-L812).

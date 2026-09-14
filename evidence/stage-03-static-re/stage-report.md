# Stage 3 — exact static loader and consumer call graph

## Gate

- Result: `PASS`
- Executor: Codex, highest available reasoning
- Completed UTC: 2026-09-14T11:43:24Z
- Stage 2 gate revision: `dff5e44b9fe9c1f0e2109b276bbadcd7edfb7deb`
- Stage 4 status: **not started**; paused by explicit user instruction

## Outcome

The exact stock read path is closed from opponent selection through the
resident destination. Two routines write selector byte `0x8009B361`:
`func_80024DC8` at `0x80024DF0` and the indirectly dispatched
`func_80038530` at `0x8003856C`. Duel state `func_8002CEE8` reads that byte and
is the sole direct caller of `func_800179F4`, which computes
`0x1D33 + 3 * selector` and requests three sectors at `0x801781D8`.

The request constructor records byte offset `sector*0x800`, count `0x1800`,
and the direct CPU destination. The scheduler reaches `func_8001455C`, which
queues Psy-Q command 6 (`DslReadN`) through `DsPacket` with callback
`0x800140A0` and retry argument `-1`. The ready callback copies exactly three
`0x800`-byte sectors through a wrapper around `CD_getsector`. Packet failures
and callback events drive retry/stall behavior; no loaded-content comparison
occurs in this path.

The only other `0x1D33 + 3 * selector` request is in `func_80020F4C` at
`0x80021124`. It copies the same three sectors to an actor-pool pointer minus
`0x1800`. Exact allocator bounds put that destination start between
`0x800EED48` and `0x800F0FD8`, proving that this auxiliary copy cannot overwrite
the canonical resident record at `0x801781D8`.

All structurally identified data now has a proven consumer except the gaps and
tail:

- array 0 at `0x801781D8` is the weighted CPU-deck pool consumed by
  `func_800243F4` to build a 40-card deck with a three-copy limit;
- arrays 1–3 at `0x8017878C`, `0x80178D40`, and `0x801792F4` are the three
  duel-reward pools consumed by `func_80021810`;
- the `0xC8` bytes at `0x801798A8` are ten rows of signed threshold/value
  pairs consumed by `func_80021558` and its ten call sites in
  `func_80021598`;
- the alignment gaps and `0x68`-byte tail have no surviving static reader, but
  are deliberately not called unused before runtime watchpoint corroboration.

The reward selector is exact: `func_80021810` computes
`0x8017878C + tier*1460`, draws `(rng & 0x7FF)+1`, accumulates up to 722
unsigned halfwords, and returns the first crossing card index plus one. It has
one direct stock caller (`0x80021C60`) and no literal function-pointer entry.
The caller selects B/C/D for rank group below 3, otherwise S/A TEC when the
side flag is nonzero and S/A POW when it is zero.

The selected card is stored at `0x8009B338`, result `+0x3C`, and
`0x801D56A8`, then passed at the sole direct stock award call
`0x80021F14`. `func_80021894` increments the save-image trunk byte, caps the
stored count at **250**, and pushes the card into the 16-entry history at
`0x801D07BC`. The resident save image is later copied by `func_8003F87C` into
the memory-card write workflow.

## Corrections and contradictions

Two material issues were preserved and resolved:

1. A recent recompilation comment says the trunk count caps at 251. Exact stock
   instructions and a byte-matching C translation write 250 when the
   incremented value reaches 251. `CON-STATIC-001` resolves to 250.
2. Lightweight constant propagation initially reported resident-record reads
   at `0x80024490/0x800244B4` and a write at `0x800244C4`. Full register data
   flow proves all three touch a stack-local card-copy counter; only the earlier
   `lhu` at `0x80024474` reads the pool. `CON-STATIC-002` records the false
   positives.

## Native-validation conclusion

No stock game-native validation of the loaded record was identified. The
proven path handles transport state, retries, and completion, but does not sum
the arrays, compare expected record bytes or IDs, compute a checksum/digest, or
verify the reward data before consuming it. This negative finding is
`CORROBORATED / Medium`, not High: it is a complete bounded static result, while
runtime alias and timing corroboration belongs to Stage 4.

This is solely a game-native conclusion. It says nothing yet about the current
RetroAchievements set, rcheevos, or supported emulator integrity behavior.

## Search completeness

- PS-X EXE identity and header mapping verified before every scan.
- Aggregate decode/xref range: CPU `0x80012800–0x800906DF`.
- Exact pointer scan: entire executable file.
- Direct callers enumerated for loader, threshold, roll, award, deck, setup,
  and save functions.
- All 21 generic request-wrapper call sites received bounded backward slices;
  every direct-memory destination was classified, with one caller-forwarded
  destination retained as a Medium-confidence dynamic boundary.
- Immediate candidates reviewed for 722, 1444, 1460, 2048, `0x7FF`, `0x1800`,
  and `0x1D33`; constructed constants reviewed in the proven functions.
- Resident readers/writers and false positives dispositioned in dedicated
  ledgers.
- No overlay address was treated as statically mapped without proof.

## Safety and privacy check

- Private executable was read only: yes.
- No emulator or RetroAchievements session was started: yes.
- Stage 4 was not started: yes.
- Only narrow instruction windows and aggregate xrefs were published: yes.
- No raw tables, executable, disc data, private paths, saves, or memory dumps
  were committed: yes.
- No bypass, concealment, anti-cheat evasion, altered-disc experiment, or
  instructions for avoiding detection were developed: yes.

## Gate checklist

- [x] Read initiator and every relevant ancestor through duel setup identified.
- [x] Source sector/index, byte count, destination, callback, and error/retry
  path proven.
- [x] Every reward-array consumer and roll caller enumerated.
- [x] Deck pool and rank-table consumers resolved.
- [x] Tier selection, weighted loop, selected-card storage, result path,
  inventory mutation, history update, and save inclusion described from stock
  instructions.
- [x] All bounded resident-range writer/reader candidates dispositioned.
- [x] Native validation searches have deterministic coverage and confidence
  ceilings.
- [x] Both contradictions resolved without discarding contrary evidence.
- [x] Public validator, unit tests, artifact hashes, prohibited-content scan,
  and whitespace checks pass.

## Sources

1. Exact accepted stock executable, minimized in `instruction-windows.csv` and
   identified by SHA-256 in `executable-map.json`.
2. Matching decompilation at revision `18bcb5806cb3dff60d3d3ee7163ce55ff6884c00`:
   [`func_80021558.c`](https://github.com/gonzaloberteri/ygofm-decomp/blob/18bcb5806cb3dff60d3d3ee7163ce55ff6884c00/src/manual/func_80021558.c),
   [`func_80021894.c`](https://github.com/gonzaloberteri/ygofm-decomp/blob/18bcb5806cb3dff60d3d3ee7163ce55ff6884c00/src/manual/func_80021894.c), and
   [`func_8003F87C.c`](https://github.com/gonzaloberteri/ygofm-decomp/blob/18bcb5806cb3dff60d3d3ee7163ce55ff6884c00/src/manual/func_8003F87C.c).
3. Historical independent layout implementation at revision
   `94d44292cfd51aa24a29b2a42131413e5f25aff2`:
   [`DataScrambler.cs`](https://github.com/forbidden-memories-coding/fmscrambler/blob/94d44292cfd51aa24a29b2a42131413e5f25aff2/FMLib/Randomizer/DataScrambler.cs#L425-L490).
4. Recent independent behavioral lead at revision
   `6b3579c6032fc59479a127824a27fc1f810e4f14`:
   [`psx_cpu_data.c`](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_cpu_data.c#L3-L22).
   Its conflicting trunk-cap comment is retained only in the contradiction
   ledger, not used as deciding evidence.
5. Original Psy-Q library documentation, public archival mirror:
   [Library Overview](https://psx.arthus.net/sdk/Psy-Q/DOCS/Devrefs/Libovr.pdf).

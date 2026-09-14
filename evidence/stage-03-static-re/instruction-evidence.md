# Narrow instruction evidence guide

`instruction-windows.csv` is the canonical machine-readable evidence. Every row
contains CPU address, PS-X EXE file offset, little-endian instruction bytes,
decoded instruction, Capstone version, and the accepted executable SHA-256.
It contains only allowlisted windows, not a replacement copy of the game.

## Load path

- `record_callsite` (`0x80017AB0–0x80017AF0`) reads signed selector
  `0x8009B361`, rejects negative values, computes `0x1D33 + 3 * selector`,
  supplies three sectors and destination `0x801781D8`, and calls
  `func_80014E1C` at `0x80017AE8`.
- `request_geometry` and `record_request` show the descriptor path. For this
  call, negative sector count `-3` becomes byte count `3 * 0x800 = 0x1800`,
  sector becomes byte offset `sector * 0x800`, and the direct CPU destination
  is retained in descriptor fields `+0x08/+0x0C`.
- `object_pool_allocation` and `auxiliary_record_request` disposition the only
  other `0x1D33` formula hit. `func_8004002C/func_800400AC` yield an actor-pool
  pointer for index 16..95; `func_80020F4C` requests the same three sectors to
  that pointer minus `0x1800`. The resulting start range
  `0x800EED48–0x800F0FD8` cannot overlap `0x801781D8`.
- `scheduler_bridge` proves the queued descriptor reaches `func_8001455C` at
  `0x80014B08`. `disc_initiation` shows sector-to-MSF conversion at
  `0x80014918` and `DsPacket` at `0x80014A1C` with mode `0xA0`, command `6`,
  callback `0x800140A0`, and retry argument `-1`.
- `sector_copy` shows the state-1 destination path calling
  `func_8007E3D0` for `0x200` words, advancing destination by `0x800`, reducing
  remaining bytes by `0x800`, and ending the ready system at zero.

The matching-decomp library map identifies `0x8007B468` as `DsPacket` and
`0x8007E3F0` as `CD_getsector`; the stock wrapper at `0x8007E3D0` calls the
latter at `0x8007E3D8`. Original Psy-Q documentation defines
`DsPacket(mode,pos,command,callback,retry_count)` as a queued command builder
and assigns command `0x06` to `DslReadN`: [Library Overview,
archival mirror](https://psx.arthus.net/sdk/Psy-Q/DOCS/Devrefs/Libovr.pdf).

## Deck, rank, and reward consumers

- `deck_consumer` constructs `0x801781D8`, generates target
  `(rng & 0x7FF)+1`, walks unsigned halfwords, emits `index+1`, rejects a card
  whose stack-local count is already three, and repeats until 40 cards exist.
- `rank_lookup` constructs `0x801798A8 + row*0x14`, reads signed threshold/value
  pairs, and returns the first value whose threshold exceeds the input.
  `rank_consumers` contains all ten direct row calls from `func_80021598`.
- `weighted_roll` constructs `0x8017878C + tier*1460`, draws a target from
  1 through 2048, accumulates 722 unsigned halfwords, returns the first
  crossing index plus one, and returns zero if no crossing occurs.
- `tier_decision` and `roll_storage` prove tier selection and the three
  selected-card destinations. `award_call` passes result `+0x3C` to the only
  direct stock call of `func_80021894`.

## Award and persistence

- `inventory_award` increments byte `0x801D024F + card_id`, writes `0xFA`
  when the incremented unsigned count is at least `0xFB`, shifts 15 history
  halfwords, and writes the new card at `0x801D07BC`.
- `save_copy` copies `0x680` bytes from `0x801D0200` into the memory-card work
  buffer before invoking `func_8003F758` with operation selector 2.
- The byte-matching decompilation independently expresses those two routines:
  [`func_80021894.c`](https://github.com/gonzaloberteri/ygofm-decomp/blob/18bcb5806cb3dff60d3d3ee7163ce55ff6884c00/src/manual/func_80021894.c) and
  [`func_8003F87C.c`](https://github.com/gonzaloberteri/ygofm-decomp/blob/18bcb5806cb3dff60d3d3ee7163ce55ff6884c00/src/manual/func_8003F87C.c).

## Completeness boundary

`direct-call-xrefs.csv` covers every decoded `jal` in CPU
`0x80012800–0x800906DF`. `pointer-xrefs.csv` searches the entire executable,
including data, for exact little-endian function addresses. These establish
the single direct callers of the roll and award routines and the literal
adjacent dispatch entries for `func_80020F4C`/`func_800218F0` and the separate
entry for `func_80038530`. They do not prove the
impossibility of a dynamically synthesized function pointer; the relevant
control flows contain no such construction, and this residual limitation is
carried into Stage 4.

`record-request-contexts.csv` additionally publishes a 14-instruction backward
slice and delay slot for every one of the 21 calls to `func_80014E1C`. Sixteen
pass no direct-memory destination. Of the five non-null cases, one is the
canonical record, one is the proven-disjoint auxiliary copy, and two resolve to
`0x80140000` and `0x80180000`. The final case at `0x80024F38` forwards caller
`a2`; its indirect entry at SLUS-FILE `0x81268` and the full literal/address
scan contain no connection to the canonical resident range. This last dynamic
boundary keeps the negative writer claim at Medium confidence.

# Preliminary Leads — Not Findings

This document preserves the strongest planning-time leads so a later executor
does not have to rediscover them. None of these claims is final. Addresses and
semantics must pass Stages 2–4 of the investigation plan against a legally
supplied NTSC-U input before being promoted beyond `LEAD` or `OBSERVED`.

## 1. Input identity leads

| Item | Planning-time value | State | Confidence | Required confirmation |
|---|---:|---|---|---|
| Game executable | `SLUS_014.11` | `LEAD` | Medium | Extract the `BOOT` value from the supplied image's `SYSTEM.CNF`. |
| Executable SHA-1 | `84747e64f6da8e764206ec203e489acf8c9dcf7d` | `LEAD` | Medium | Recompute locally and match the decompilation target.[^decomp-readme] |
| RA game ID | `11388` | `OBSERVED` | High for 2026-09-13 | Refresh the official game and hash pages.[^ra-game] |
| Registered RA hash | `b181396315dc9dd3656d5910ea65239b` | `OBSERVED` | High for 2026-09-13 | Recompute with pinned rcheevos and compare with the current official hash page.[^ra-hashes] |

The RA game page, achievement count, hash list, code notes, and supported
emulator list are live state. A date-stamped observation is not a permanent
fact.

## 2. Candidate disc record

A recent recompilation project describes one 6144-byte (three-sector) record
per opponent at WA-relative sector `0x1D33 + 3 * opponent_id`, loaded to
`0x801781D8` before a duel by candidate routine `func_800179F4`.[^cpu-data]
Its comments and constants describe four 722-entry little-endian `u16` arrays,
each occupying 1444 bytes inside a 1460-byte stride.[^cpu-layout]

Under that hypothesis:

```text
WA-relative record start = (0x1D33 + 3 * opponent_id) * 0x800
absolute DISC-LBA        = 10102 + 0x1D33 + 3 * opponent_id
RAM record start         = 0x801781D8
RAM record length        = 0x1800
```

The project uses IDs `1..39`. Therefore the ID-1 record would start at
WA offset `0xE9B000` and absolute LBA `17580`. A much older, independent data
scrambler also places its first duelist at `0xE9B000` with subsequent records
`0x1800` bytes apart, and writes the three reward arrays at `+0x5B4`, `+0xB68`,
and `+0x111C`.[^fmscrambler] This agreement raises the layout lead above a
single-project guess, but it does not yet prove the loader routine or semantic
use in the stock executable.

### Candidate resident-memory map

| Region | CPU-KSEG0 inclusive range | RA inclusive range | Length | Interpretation lead |
|---|---|---|---:|---|
| Whole record | `0x801781D8–0x801799D7` | `0x1781D8–0x1799D7` | `0x1800` | Current opponent record |
| Deck weights | `0x801781D8–0x8017877B` | `0x1781D8–0x17877B` | `0x5A4` | 722 `u16` weights |
| Gap 0 | `0x8017877C–0x8017878B` | `0x17877C–0x17878B` | `0x10` | Alignment/unknown |
| Tier 0 | `0x8017878C–0x80178D2F` | `0x17878C–0x178D2F` | `0x5A4` | S/A POW reward weights |
| Gap 1 | `0x80178D30–0x80178D3F` | `0x178D30–0x178D3F` | `0x10` | Alignment/unknown |
| Tier 1 | `0x80178D40–0x801792E3` | `0x178D40–0x1792E3` | `0x5A4` | B/C/D reward weights |
| Gap 2 | `0x801792E4–0x801792F3` | `0x1792E4–0x1792F3` | `0x10` | Alignment/unknown |
| Tier 2 | `0x801792F4–0x80179897` | `0x1792F4–0x179897` | `0x5A4` | S/A TEC reward weights |
| Gap 3 | `0x80179898–0x801798A7` | `0x179898–0x1798A7` | `0x10` | Alignment/unknown |
| Candidate rank data | `0x801798A8–0x8017996F` | `0x1798A8–0x17996F` | `0xC8` | 200-byte table; semantics unverified |
| Trailing bytes | `0x80179970–0x801799D7` | `0x179970–0x1799D7` | `0x68` | Unknown/possibly unused |

The CPU-to-RA conversion above is supported by rcheevos' PlayStation map, in
which logical addresses `0x000000–0x1FFFFF` represent the console's two
megabytes of RAM.[^psx-map] Stage 2 must independently recalculate every range
and test both endpoints.

## 3. Candidate load chain

The proposed pre-duel chain is:

```text
Main_RunDuel
  -> func_800179F4                 candidate orchestration/duel loader
       -> func_80014E1C            candidate sector/file streaming helper
            -> reads three sectors from WA_MRG.MRG
            -> destination 0x801781D8
```

Only the function boundary for `func_800179F4` is presently corroborated by the
matching-decompilation project's split configuration; the role and full caller/
callee semantics remain to be proven from stock instructions and traces.
Executors must not rename these functions as established facts before Stage 3.

## 4. Candidate interpretation and award chain

The strongest current lead is this end-of-duel chain:

```text
func_800218F0                 result/rank/reward state candidate
  -> derives tier 0, 1, or 2 from result bytes
  -> func_80021810(tier)      candidate weighted reward roll
       table = 0x8017878C + tier * 0x5B4
       roll  = (RNG & 0x7FF) + 1
       accumulate 722 u16 weights
       return first card index whose cumulative total reaches roll
  -> stores chosen card at candidate result+60 = 0x80179A14
  -> func_80021894(card_id)   candidate card award
       increments trunk byte at 0x801D024F + card_id, capped at 251
```

These behaviors are described by the recent recompilation's trace-derived
comments and constants.[^drop-functions] The matching decompilation does contain
a manual `func_80021894` implementation and a boundary for `func_800218F0`, but
the complete stock call chain and `func_80021810` interpretation must still be
recovered and compared instruction-for-instruction.

The proposed tier mapping is:

| Tier | Proposed rank class |
|---:|---|
| `0` | S/A POW |
| `1` | B/C/D |
| `2` | S/A TEC |

That mapping is currently sourced from a project comment identifying the
decision range as `0x80021A4C–0x80021C58`; it is not final evidence.[^tier-map]

### Adjacent downstream candidates

| CPU-KSEG0 address | RA address | Lead |
|---|---|---|
| `0x80179A14` | `0x179A14` | Chosen reward card in the results block |
| `0x8009B361` | `0x09B361` | Opponent ID |
| `0x8009B365` | `0x09B365` | Free-duel flags |
| `0x800E9FF0` | `0x0E9FF0` | Rank calculation block |
| `0x801D024F + card_id` | `0x1D024F + card_id` | Trunk quantity byte |
| `0x801D07E0` | `0x1D07E0` | Star-chip total |
| `0x800FE6F8` | `0x0FE6F8` | RNG seed candidate |

These addresses are important to Stage 6 even if the RA set never reads the
source weights. Reading a chosen card, rank, opponent, inventory count, or chip
total is a **derived dependency**, not validation of the reward arrays.

## 5. RA hash-boundary lead

Pinned rcheevos source currently:

1. locates `SYSTEM.CNF`;
2. parses the `BOOT` executable path;
3. reads the PS-X EXE payload length from header offset 28 and adds the 2048-byte
   header;
4. computes MD5 over the boot executable name/path followed by that many
   executable bytes.[^rcheevos-hash]

Under that implementation, unrelated `WA_MRG.MRG` bytes are not direct inputs
to the normal PlayStation identification hash. This is a source-grounded lead,
not yet a complete answer to the integrity question: Stages 7–9 must still
check client session behavior, media changes, current emulator integrations,
optional verification features, game-native checks, and runtime monitoring.

DuckStation independently implements a separate RA hash over executable name
and the PS-X EXE header-declared extent.[^duck-ra-hash] It also calculates an
internal 64-bit game hash that includes the executable, ISO primary volume
descriptor, and track length.[^duck-internal-hash] The latter must not be
reported as an RA integrity check unless a traced enforcement path proves that
it controls the RA session.

## 6. Open questions that the execution must settle

- Is `func_800179F4` the direct owner of the three-sector read, or only an
  ancestor? What are the exact call sites, arguments, destination, and error
  paths?
- Does one read cover the full 6144-byte record, or do helpers split it?
- Which stock instructions consume the deck, each reward tier, candidate rank
  table, gaps, and trailing bytes?
- Is `func_80021810` uniquely called by `func_800218F0`, and do all award paths
  pass through `func_80021894`?
- Which current RA assets directly read the record, indirectly reach it, or read
  only downstream reward state?
- Does any supported frontend/core re-identify or validate the disc other than
  at initial load and media change?
- Does the game itself validate table totals, record identity, sector contents,
  or loaded code?
- Can each installed emulator binary be mapped to the reviewed source revision?

## Sources

[^decomp-readme]: [gonzaloberteri/ygofm-decomp README at `18bcb580`](https://github.com/gonzaloberteri/ygofm-decomp/blob/18bcb5806cb3dff60d3d3ee7163ce55ff6884c00/README.md)
[^ra-game]: [RetroAchievements game 11388](https://retroachievements.org/game/11388)
[^ra-hashes]: [RetroAchievements hashes for game 11388](https://retroachievements.org/game/11388/hashes)
[^cpu-data]: [Recent recompilation, `psx_cpu_data.c` lines 3–16](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_cpu_data.c#L3-L16)
[^cpu-layout]: [Recent recompilation, `psx_cpu_data.c` lines 104–123](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_cpu_data.c#L104-L123)
[^fmscrambler]: [fmscrambler, `DataScrambler.cs` lines 431–487](https://github.com/forbidden-memories-coding/fmscrambler/blob/94d442aed94bb30c74bb0d8fcc87209028d1acff/FMLib/Randomizer/DataScrambler.cs#L431-L487)
[^psx-map]: [rcheevos PlayStation memory map, `consoleinfo.c` lines 805–812](https://github.com/RetroAchievements/rcheevos/blob/c28462eafdbeb881a1d442754dd17aae5c4ab834/src/rcheevos/consoleinfo.c#L805-L812)
[^drop-functions]: [Recent recompilation, `psx_card_drops.c` lines 61–108](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_card_drops.c#L61-L108)
[^tier-map]: [Recent recompilation, `psx_drop_missing.c` lines 3–18](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_drop_missing.c#L3-L18)
[^rcheevos-hash]: [rcheevos PlayStation hashing, `hash_disc.c` lines 866–978](https://github.com/RetroAchievements/rcheevos/blob/c28462eafdbeb881a1d442754dd17aae5c4ab834/src/rhash/hash_disc.c#L866-L978)
[^duck-ra-hash]: [DuckStation RA hash, `system.cpp` lines 906–928](https://github.com/stenzek/duckstation/blob/96268ab66aa60c434c512bba19d45c75fa7a1b36/src/core/system.cpp#L906-L928)
[^duck-internal-hash]: [DuckStation internal game hash, `system.cpp` lines 892–903](https://github.com/stenzek/duckstation/blob/96268ab66aa60c434c512bba19d45c75fa7a1b36/src/core/system.cpp#L892-L903)

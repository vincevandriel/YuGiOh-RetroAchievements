# Stage 2 derivation report

## Coordinate systems

All disc arithmetic uses ISO9660 user-data sectors of 2048 bytes. The raw
MODE2/2352 track geometry is used only by the extraction layer established in
Stage 1. `WA_MRG.MRG` begins at absolute disc LBA 10102; offsets in the Stage 2
CSVs are relative to its extracted 2048-byte user-data stream.

For a selected opponent ID `id` in `1..39`:

```text
WA sector       = 0x1D33 + 3 * id
WA byte start   = WA sector * 0x800
absolute LBA    = 10102 + WA sector
record length   = 3 * 0x800 = 0x1800
```

This yields ID 1 at WA offset `0xE9B000`, absolute LBA 17580, and ID 39 at
`0xED4000`, absolute LBA 17694. The final byte of the selected range is
`0xED57FF`, in absolute LBA 17696.

## Independent derivations

1. **Exact stock executable.** In the accepted `SLUS_014.11`, the instruction
   sequence at CPU `0x80017AB0–0x80017AEC` reads a signed byte from
   `0x8009B361`, rejects a negative value, computes `0x1D33 + 3 * value`, sets
   an argument to three, places `0x801781D8` in the seventh argument slot, and
   calls `0x80014E1C`. `stock-layout-xref.csv` is regenerated from the exact
   executable only after checking its Stage 1 SHA-256.
2. **Historical direct-offset implementation.** The independently developed
   FMScrambler loops over 39 entries using `0xE9B000 + 0x1800 * i`, and accesses
   1444-byte arrays at `+0x0000`, `+0x05B4`, `+0x0B68`, and `+0x111C`.
3. **Private-data structural scan.** Without using labels, the scanner tests
   every sector-aligned `0x1800`-byte candidate for four 722-word arrays at
   those offsets whose sums are 2048. It contains the complete formula-derived
   window and validates every boundary and statistic.

The first two derivations agree on all 39 record boundaries. The third supports
the structure but exposes an important ambiguity instead of independently
labelling ID 1.

## Recorded ambiguity

The structural scan finds 40 consecutive valid records, beginning one record
earlier at `0xE99800`. Therefore there are two 39-record windows. The extra
predecessor is byte-for-byte identical to the selected ID-1 record; its record
and all four array SHA-256 values match ID 1 exactly.

This falsifies the preliminary assumption that weight-array structure would
uniquely identify ID 1. It does not move the selected start: the exact stock
sector formula and the historical direct-offset implementation both identify
`0xE9B000`. The purpose of the predecessor remains unknown for Stage 3.

## Record schema and statistics

Each selected record partitions exactly into:

- four `0x5A4`-byte candidate arrays at `+0x0000`, `+0x05B4`, `+0x0B68`, and
  `+0x111C`;
- four `0x10`-byte intervening regions;
- a `0xC8`-byte candidate rank region at `+0x16D0`;
- an unknown `0x68`-byte tail at `+0x1798`.

All 156 arrays have 722 little-endian `u16` entries and sum to 2048. Their
nonzero counts range from 13 through 169. Only boundaries, aggregate
statistics, and cryptographic digests are published.

## RAM and RetroAchievements coordinates

The exact caller supplies candidate destination `0x801781D8`. A `0x1800`-byte
record therefore ends at `0x801799D7`. Masking the KSEG0 alias to 2 MiB physical
RAM gives `0x1781D8–0x1799D7`. Pinned rcheevos exposes PlayStation system RAM
without an offset transformation in this range, so the RA coordinates are the
same. `boundary-tests.json` records one-byte, end-byte, crossing, and first-byte
outside vectors for each subregion.

## Semantic limit

Stage 2 confirms the byte geometry and addresses. The labels “deck,” “S/A POW,”
“B/C/D,” “S/A TEC,” and “rank” remain leads from secondary reverse-engineering
sources. They will not become confirmed until Stage 3 proves the loader/callee
and Stage 4 proves the stock consumers and award path.

## Sources

1. Exact accepted private `SLUS_014.11`, SHA-256
   `84a54ed74f3d0edd6d81380839f7e4ef5bfb21ecea18be9a062bd6bfa5a45c88`,
   narrow disassembly in `stock-layout-xref.csv`.
2. FMScrambler,
   [`DataScrambler.cs` lines 425–490 at `94d4429`](https://github.com/forbidden-memories-coding/fmscrambler/blob/94d44292cfd51aa24a29b2a42131413e5f25aff2/FMLib/Randomizer/DataScrambler.cs#L425-L490).
3. YuGiOhForbiddenMemoriesRecomp,
   [`psx_cpu_data.c` lines 3–22](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_cpu_data.c#L3-L22)
   and [109–123 at `6b3579c`](https://github.com/Unchiga/YuGiOhForbiddenMemoriesRecomp/blob/6b3579c6032fc59479a127824a27fc1f810e4f14/src/psx_cpu_data.c#L109-L123).
4. rcheevos,
   [`consoleinfo.c` lines 805–812 at `c28462e`](https://github.com/RetroAchievements/rcheevos/blob/c28462eafdbeb881a1d442754dd17aae5c4ab834/src/rcheevos/consoleinfo.c#L805-L812).

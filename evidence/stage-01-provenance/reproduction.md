# Stage 1 reproduction

Private paths are represented by labels. Supply them only through ignored local
configuration or process-local variables and do not echo them.

## STAGE1-REPRO-001 — Identify and extract the stock input

1. Hash the private CUE and MODE2/2352 track with SHA-1 and SHA-256.
2. Verify the raw track size is an exact multiple of 2352.
3. Using `tools/extract_disc.py` from
   `gonzaloberteri/ygofm-decomp@18bcb5806cb3dff60d3d3ee7163ce55ff6884c00`,
   extract into an isolated ignored workspace.
4. Verify the ISO9660 PVD at LBA 16 and enumerate all file extents.
5. Read the extracted `SYSTEM.CNF` and confirm
   `BOOT = cdrom:\SLUS_014.11;1`.
6. Hash `SYSTEM.CNF`, `SLUS_014.11`, and `DATA/WA_MRG.MRG`.
7. Parse the PS-X EXE header as little-endian values. Require marker `PS-X EXE`,
   load address `0x80010000`, declared text size 1900544, and extracted size
   `2048 + declared text size = 1902592`.
8. Compare the whole-track and executable SHA-1 values to the pinned
   matching-decompilation README.

Expected result: every value equals `input-manifest.json`; no proprietary file
is copied into the audit repository.

## STAGE1-REPRO-002 — Recompute the rcheevos PlayStation hash

1. Check out
   `RetroAchievements/rcheevos@c28462eafdbeb881a1d442754dd17aae5c4ab834`.
2. Compile `tools/hash_psx.c` with that checkout's `hash.c`, `hash_disc.c`,
   `cdreader.c`, `md5.c`, and `rc_compat.c`. Disable unrelated ROM, ZIP, and
   encrypted hash modules at compile time.
3. Run the resulting local helper against the private CUE.
4. Require exit code 0 and output exactly
   `b181396315dc9dd3656d5910ea65239b`.
5. Compare the result with the current official supported-hash page.

The helper does not implement or restate the hash algorithm; it invokes the
pinned rcheevos API and does not echo the private path.

## STAGE1-REPRO-003 — Refresh official public state

Read the following official pages in the same observation window:

- <https://retroachievements.org/game/11388>
- <https://retroachievements.org/game/11388/hashes>
- <https://retroachievements.org/codenotes.php?g=11388>
- <https://docs.retroachievements.org/general/emulator-support-and-issues.html>

Record only stable scoped fields and UTC time. Exclude current player activity
and account-specific information. Expected values for this snapshot are 216
core achievements, 1220 points, one registered hash, 164 code notes, and four
supported PlayStation implementations.

## STAGE1-REPRO-004 — Inventory local emulator binaries

1. From the configured emulator root, hash the frontend executable and each
   PlayStation core library.
2. Record size and UTC modification time.
3. Read adjacent core-info metadata and PE version fields without launching a
   game.
4. Search the configured core directory for Beetle PSX HW and Beetle PSX.
5. Check the configured emulator root and Windows uninstall registrations for
   DuckStation.
6. Record `NOT_DISCOVERED` rather than claiming system-wide absence.

Expected result: the rows and hashes in `emulator-binaries.csv` reproduce. No
configuration value is changed and no emulator game session is started.

## STAGE1-REPRO-005 — Verify source pins

For every source in `sources.lock.json`, fetch `origin`, verify the pinned object
is a commit, compare local HEAD with `origin/HEAD`, and require a clean worktree.
Expected result: every row in `source-verification.json` is true.

## STAGE1-REPRO-006 — Gate integrity

Parse all JSON and CSV artifacts, compare ledger headers to the templates,
recompute `artifacts.sha256`, run the Stage 0 prohibited-file/secret scan, and
run the Git whitespace check. Any discrepancy fails the gate.

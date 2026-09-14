# R2 Eligibility After R1

R1 passed on 2026-09-14T23:05:32Z after two ignored local copies of the
accepted private BIN/CUE input reproduced its recorded descriptor and track
digests. R2 workstreams may proceed only according to their individual
readiness states below. Canonical Stage 4 has not begun.

## R2-A — Stock dynamic trace

Blocked on a verified read-only breakpoint/watchpoint workflow with
RetroAchievements disabled before the game is booted. The stock input identity
is verified and must be rechecked immediately before any future boot.

The supplied disc must be treated only as a stock identity check. It will not
be modified, connected to RA during debugging, or used for any evasion test.

## R2-B — Current RA definition snapshot

Blocked pending an authorized normal-client or toolkit export route for the
complete active achievement, leaderboard, and Rich Presence definitions. Do
not provide or commit a token, cookie, password, request header, or raw
authenticated response. The raw snapshot remains in ignored local evidence;
only sanitized metadata and definition digests may enter Git.

## R2-C — Client and emulator evidence inventory

This workstream is ready. Its inputs already include clean,
pinned local rcheevos, RetroArch, DuckStation, RAWeb, documentation, and game
reverse-engineering sources, plus the current hashes of the installed
RetroArch/SwanStation binaries.

Known boundaries to retain:

- installed RetroArch and SwanStation binaries are source-unmapped;
- Beetle PSX HW, Beetle PSX, and standalone DuckStation are not available in
  the configured emulation scope;
- source review may proceed, but installed-binary negative claims remain capped
  at Medium confidence until exact source mapping is established.

It may begin using the bounded source and binary inventory procedure. It does
not authorize a dynamic game run or a claim about source-unmapped binaries.

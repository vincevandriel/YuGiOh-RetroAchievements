# R2 Eligibility After R1

R1 has not passed because the exact accepted private disc input has not been
re-located. No canonical Stage 4–9 work may begin while that blocker remains.

## R2-A — Stock dynamic trace

Blocked pending both of the following:

1. the ignored local location of `PRIVATE_DISC_NTSC_U_TRACK_01`, so its known
   CUE and whole-track digests can be reverified; and
2. a verified read-only breakpoint/watchpoint workflow with RetroAchievements
   disabled before the game is booted.

The supplied disc must be treated only as a stock identity check. It will not
be modified, connected to RA during debugging, or used for any evasion test.

## R2-B — Current RA definition snapshot

Blocked pending an authorized normal-client or toolkit export route for the
complete active achievement, leaderboard, and Rich Presence definitions. Do
not provide or commit a token, cookie, password, request header, or raw
authenticated response. The raw snapshot remains in ignored local evidence;
only sanitized metadata and definition digests may enter Git.

## R2-C — Client and emulator evidence inventory

This workstream is ready after R1 resumes. Its inputs already include clean,
pinned local rcheevos, RetroArch, DuckStation, RAWeb, documentation, and game
reverse-engineering sources, plus the current hashes of the installed
RetroArch/SwanStation binaries.

Known boundaries to retain:

- installed RetroArch and SwanStation binaries are source-unmapped;
- Beetle PSX HW, Beetle PSX, and standalone DuckStation are not available in
  the configured emulation scope;
- source review may proceed, but installed-binary negative claims remain capped
  at Medium confidence until exact source mapping is established.

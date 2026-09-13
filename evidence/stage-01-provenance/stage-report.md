# Stage 1 — Input, source, binary, and live-state provenance

## Gate

- Result: `PASS`
- Executor: Codex, highest available reasoning
- Started UTC: 2026-09-13T21:34:00Z
- Completed UTC: 2026-09-13T21:42:47Z
- Stage 0 gate revision: `b3574da`

## Objective

Identify the exact stock NTSC-U input, verify its boot executable and
`WA_MRG.MRG`, recompute the registered RA hash with pinned rcheevos, refresh
official live state, pin source revisions, and inventory available emulator
binaries without modifying private inputs or emulator/RA state.

## Results

The private USA BIN/CUE is accepted. Its whole-track SHA-1 and extracted
`SLUS_014.11` SHA-1 match the matching-decompilation references. `SYSTEM.CNF`
boots `SLUS_014.11`; the executable's declared text extent plus header exactly
matches its extracted size. `WA_MRG.MRG` is identified at LBA 10102 with a
37748736-byte extent and private-content digest recorded in the public manifest.

A minimal local driver compiled against pinned rcheevos produced
`b181396315dc9dd3656d5910ea65239b`, exactly matching the sole hash on the
official supported-hash page. This confirms input identity; it does not yet
answer the broader Stage 7 integrity-boundary question.

The official live snapshot remains 216 core achievements, 1220 points, one
registered hash, and 164 code notes. The current supported PlayStation list is
Beetle PSX HW, Beetle PSX, SwanStation, and DuckStation.

The configured local installation contains RetroArch and SwanStation. Their
binary hashes are recorded, but their exact source revisions are not currently
recoverable from embedded metadata; later negative claims about those binaries
are therefore capped at Medium confidence. No Beetle core was present in the
configured core directory, and no DuckStation installation was found in the
configured emulator root or uninstall registrations. Those are discovery-scope
observations, not system-wide absence claims.

All eight source pins were fetched, existed as commits, matched their origin
default branches, and had clean worktrees at verification time.

## Contradictions and unresolved items

No Stage 1 contradiction is open. These limitations carry forward:

- installed RetroArch and SwanStation binaries are source-unmapped;
- Beetle PSX HW, Beetle PSX, and DuckStation are not locally available in the
  discovery scope;
- authenticated achievement definitions and code-note bodies are deferred to
  Stage 5;
- all live RA observations require later freshness checks.

## Safety and privacy check

- Source image and extracted files were read only: yes.
- Extraction occurred only in an isolated ignored private workspace: yes.
- No proprietary byte or private absolute path was added to Git: yes.
- No emulator game session was started: yes.
- No RA login, unlock, leaderboard submission, or authenticated request was
  performed: yes.
- No emulator, game, save, or RA configuration was changed: yes.
- No modified target or evasion experiment was performed: yes.

## Gate checklist

- [x] Private input is conclusively NTSC-U and matches the targeted executable.
- [x] Boot executable and RA hash match the current registered game.
- [x] Source and tool versions are immutable or explicitly versioned.
- [x] Official live state has a UTC timestamp and source URLs.
- [x] Every available tested binary has size, time, and SHA-256.
- [x] Missing/source-unmapped emulators have explicit confidence limits.
- [x] Artifact hashes and repository scans are reverified after staging.
- [x] No private/copyrighted input or credential is committed.

## Sources

1. RetroAchievements, [Yu-Gi-Oh! Forbidden Memories](https://retroachievements.org/game/11388).
2. RetroAchievements, [Supported Game Hashes](https://retroachievements.org/game/11388/hashes).
3. RetroAchievements, [Code Notes](https://retroachievements.org/codenotes.php?g=11388).
4. RetroAchievements, [Emulator Support](https://docs.retroachievements.org/general/emulator-support-and-issues.html).
5. RetroAchievements/rcheevos,
   [`hash_disc.c` at `c28462e`](https://github.com/RetroAchievements/rcheevos/blob/c28462eafdbeb881a1d442754dd17aae5c4ab834/src/rhash/hash_disc.c#L866-L978).
6. gonzaloberteri/ygofm-decomp,
   [README at `18bcb58`](https://github.com/gonzaloberteri/ygofm-decomp/blob/18bcb5806cb3dff60d3d3ee7163ce55ff6884c00/README.md#L7-L14).

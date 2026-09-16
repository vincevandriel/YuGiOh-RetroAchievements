# R2-C reproduction

All commands below are read-only against source checkouts and configured local
binary files. They must not launch an emulator, access authenticated
RetroAchievements state, or consume private disc data.

## R2C-REPRO-001 — Verify source pins and selected files

1. From the workspace-level `work/sources` directory, use `git rev-parse HEAD`
   and `git status --porcelain` for rcheevos, RA docs, RAWeb, RetroArch, and
   DuckStation.
2. Require each revision in `input-manifest.json` and an empty status result.
3. Compute SHA-256 for every file under
   `selected_source_file_sha256`; require exact equality.

## R2C-REPRO-002 — Refresh the supported integration list

1. Open the official RetroAchievements emulator-support page.
2. Read the current PlayStation table and compare the entries with
   `official_supported_playstation_integrations`.
3. If an entry differs, record a freshness delta and add a matrix row. Do not
   silently reuse this snapshot for Stage 8 closure.

## R2C-REPRO-003 — Reproduce configured-scope binary inventory

1. Hash the configured RetroArch executable and any discovered PlayStation core
   libraries.
2. Compare the results with
   `evidence/stage-01-provenance/emulator-binaries.csv` and
   `binary-source-map.csv`.
3. Record `NOT_DISCOVERED` only for the configured scope; do not claim that a
   binary is absent elsewhere.

## R2C-REPRO-004 — Reproduce candidate locations

Run exact-symbol searches for the symbols in `source-locations.csv` against
the pinned source files. Confirm each listed file and line range. A positive
search is a candidate location only; it does not prove a content check or a
reachable released-binary path.

## R2C-REPRO-005 — Preserve bundled-source provenance

Hash the selected upstream and RetroArch-bundled `rc_client.c` and
`hash_disc.c` files. Require the equality/difference relationship recorded by
`R2C-INV-005`. Review implementation differences before reusing upstream
source conclusions for a RetroArch integration row.

## R2C-REPRO-006 — Reproduce initial integrity-hit coverage

1. Run the exact `R2C-SEARCH-007` terms against each pinned source tree.
2. Require the original file-count partition: seven rcheevos, two RetroArch,
   nine DuckStation, and seven RAWeb files.
3. Require `integrity-hit-dispositions.csv` to contain twelve dispositions
   whose `source_files` fields account for exactly 25 file entries.
4. Check that each disposition is source-only and preserves the limitations
   stated in `consumer-review-notes.md`. Do not turn a keyword hit into a
   binary or enforcement conclusion.

## R2C-REPRO-007 — Refresh support-list coverage

1. Open the official RetroAchievements emulator-support page and read its
   PlayStation table.
2. Compare the current entries with `support-refresh.md` and the four rows of
   `binary-source-map.csv`.
3. Record a freshness delta if the list changes. Do not silently retain an old
   list for a Stage 8 or Stage 11 closure.

## R2C-REPRO-008 — Reproduce the R2-C coverage decision

1. Validate every row of `acquisition-coverage.csv` against the referenced
   artifact.
2. Require all `PASS` and `EXPLICITLY_UNAVAILABLE` rows to have a cited input.
3. Require every `BLOCKED-INPUT` row to name its missing input and the affected
   claim boundary. A source-unmapped binary must not be promoted to a
   source-mapped integration by inference.

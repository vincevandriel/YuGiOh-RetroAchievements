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

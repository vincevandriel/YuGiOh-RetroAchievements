# R3-A — rcheevos source call graphs and neutral fixture specification

## Status

`COMPLETE-SOURCE-ONLY` as of 2026-09-20T11:43:34Z.

This bounded R3 increment completes the static call-graph and fixture-design
portion of the next eligible work. It does not run a fixture, build rcheevos,
launch an emulator, open any game media, access an authenticated service, or
change the status of R2-A, R2-B, R2-C, or R3 as a whole.

## What this packet establishes

- The pinned upstream PlayStation hashing path and its statically derived input
  boundary are recorded in `psx-hash-callgraph.mmd` and `hash-inputs.csv`.
- Pinned `rc_client` initial-load, session-start, frame, explicit-media-change,
  reset, progress-deserialization, award, and leaderboard paths are recorded
  in `client-session-callgraph.mmd`, `rehash-triggers.csv`, and
  `per-frame-read-path.md`.
- The planned neutral fixtures A0–A6 are specified in
  `synthetic-psx-fixture-spec.md`, including source-derived expected relations,
  safety gates, and fail conditions. Their execution is `NOT_RUN`.

## Boundaries that remain controlling

- Findings apply only to rcheevos revision
  `c28462eafdbeb881a1d442754dd17aae5c4ab834` and the selected source files.
- `RC_CLIENT_SUPPORTS_EXTERNAL` dispatches are explicitly retained as an
  external-client boundary, not treated as covered upstream behavior.
- The actual current achievement, leaderboard, and Rich Presence definitions
  are unavailable; therefore the concrete per-frame address set remains
  `UNKNOWN` rather than empty.
- No installed frontend or core binary is source-mapped. No source result is an
  installed-binary behavior claim.
- No conclusion about deployed RetroAchievements server behavior is made from
  the client request construction paths.

## Packet contents

- `input-manifest.json` — source pins and selected source/test file digests.
- `source-locations.csv` — exact file/line inventory for the bounded graph.
- `psx-hash-callgraph.mmd` and `hash-inputs.csv` — identification path and
  source-derived input disposition.
- `client-session-callgraph.mmd`, `rehash-triggers.csv`, and
  `per-frame-read-path.md` — lifecycle and memory-read evidence.
- `synthetic-psx-fixture-spec.md` — neutral A0–A6 implementation contract;
  not an executed test result.
- `facts.csv`, `contradictions.csv`, `reproduction.md`, and
  `validation-results.json` — evidence ledger and reproducibility controls.

R3 cannot close from this packet. The remaining R3 work requires neutral
fixture implementation/execution, the separately blocked R2 inputs, and the
confidence ceilings recorded in R2-C.

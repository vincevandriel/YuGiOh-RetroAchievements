# Planned audit tooling contracts

The investigation may implement these tools as stages begin. This file defines
their interfaces and failure behavior in advance so a light or medium executor
does not have to redesign the workflow.

Tool names are contracts, not claims that implementation is complete.

Implemented support utility:

- `hash_psx.c` — a minimal read-only driver that invokes a selected rcheevos
  revision's PlayStation hash API. It does not implement the algorithm itself
  and does not echo the private input path.

## `snapshot-public-state`

**Stage:** 1 and 11
**Input:** official game ID `11388` and official documentation URLs
**Output:** normalized `public-state.json` with UTC timestamp, page URLs,
achievement/point/hash/code-note counts, supported-emulator entries, and a
SHA-256 of each normalized observation
**Must fail when:** a required page is unavailable, the game ID differs, a
field cannot be parsed, or the previous snapshot changed without an explicit
`changed` result.

## `verify-private-inputs`

**Stage:** 1
**Input:** private disc path supplied outside Git
**Output:** public metadata only: format, size, SHA-1/SHA-256, `SYSTEM.CNF` boot
path, extracted-file sizes/hashes, PS-X EXE header fields, and rcheevos hash
**Must fail when:** the boot executable is not `SLUS_014.11`, an expected hash
does not match, a file is truncated, or the output would contain private paths
or bytes.

## `derive-record-layout`

**Stage:** 2
**Input:** ignored private `WA_MRG.MRG`, ISO extent metadata, opponent ID range
**Output:** disc layout, derived array statistics/hashes, and boundary vectors
**Must fail when:** an access is out of bounds, the sector unit is ambiguous,
record/array sizes disagree, or a private byte array is directed to tracked
output.

## `map-slus-addresses`

**Stage:** 3
**Input:** ignored private `SLUS_014.11`, verified PS-X EXE header, address list
**Output:** file-offset/CPU/PS1-RAM/RA conversions with raw instruction words
for narrow requested ranges
**Must fail when:** a range is outside the declared executable, an overlay is
treated as the base executable, or forward/reverse conversion differs.

## `normalize-ra-assets`

**Stage:** 5–6
**Input:** ignored authorized game-data response and pinned rcheevos parser
**Output:** sanitized manifest and normalized operands for achievements,
leaderboards, and Rich Presence
**Must fail when:** any asset fails parsing, bytes remain unconsumed, counts do
not reconcile, account data remains, or raw definitions are written to tracked
output without explicit publication review.

## `classify-address-dependencies`

**Stage:** 6
**Input:** normalized operands plus target ranges and boundary vectors
**Output:** overlap rows, indirect-range analysis, and `A`–`F` classifications
**Must fail when:** an indirect address is unbounded but labeled `F`, a
multi-byte overlap is missed, or an asset is unclassified.

## `build-synthetic-psx-fixtures`

**Stage:** 9
**Input:** deterministic seed and generated payload sizes
**Output:** fully synthetic PS1 images, source manifests, and expected relation
assertions; absolutely no game-derived input is accepted
**Must fail when:** an input file outside the generator's own output directory
is requested, determinism fails, or a fixture contains a known target-game
signature.

## `verify-hash-boundary`

**Stage:** 7–9
**Input:** generated fixture manifest and one or more hash implementations
**Output:** hashes plus relation assertions (`same-as-A0`, `different-from-A0`,
or `expected-error`)
**Must fail when:** a relationship differs, an implementation errors
unexpectedly, or only printed values—not assertions—are produced.

## `validate-evidence`

**Stage:** every gate, especially 10–11
**Input:** repository root and stage/release manifest
**Output:** machine-readable results for required files, CSV/JSON schemas,
fact references, artifact hashes, internal links, contradictions, private-file
signatures, and secrets
**Must fail when:** anything required is missing; a hash differs; an evidence
reference is dangling; a high-impact contradiction is open; or prohibited data
is detected.

## General implementation rules

- Tools must run non-interactively after private input locations are supplied
  through an ignored configuration or process-local environment value.
- Never print credentials, cookies, headers, private absolute paths, or raw game
  bytes.
- Emit UTF-8 JSON/CSV with stable key/column ordering and UTC ISO 8601 times.
- Use nonzero exit status for every failed assertion.
- Record tool version and Git revision in each output.
- Add unit tests for success, malformed input, out-of-bounds input, privacy
  redaction, and deterministic regeneration.
- Scripts may support read-only stock analysis and synthetic fixtures only.
  Reject options whose purpose is altering the target game or evading integrity
  behavior.

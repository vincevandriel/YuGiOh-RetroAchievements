# R2-C — Client and emulator evidence inventory

This is the acquisition packet for **R2-C** in
`docs/REMAINDER_EXECUTION_PLAN.md`. It records exact revisions, selected source
file digests, candidate lifecycle locations, and binary/source boundaries for
the current supported PlayStation integrations.

## Status

`BLOCKED-INPUT` as of 2026-09-16T02:01:05Z.

The first bounded source-review pass is complete. It resolved the selected
RetroArch bundled-source provenance difference and added the initial
load/frame/media/reset/memory-reader skeleton. The bounded integrity-keyword
consumer review is also complete: all 25 initial file hits are dispositioned in
`integrity-hit-dispositions.csv`. The acquisition/coverage audit is now also
complete. It established that the source inventory is complete for the current
four-entry public support list, but it cannot close R2-C: the installed
RetroArch and SwanStation binaries are not source-mapped, while the two Beetle
cores and standalone DuckStation are unavailable in the configured local
scope. Those input gaps are now an explicit phase block rather than an implied
negative conclusion.

The packet intentionally does **not** close canonical Stages 7 or 8. It does
not claim that an unreviewed candidate path is reachable in a released binary,
that a source-only path represents an installed binary, or that a feature gate
is a content-integrity check. R3 must trace consumers, classify the paths, and
run the planned safe fixture tests before any bounded negative conclusion.

## Scope and safety boundary

- The source review is read-only. No game, emulator, authenticated client, or
  achievement asset was launched or modified.
- No credential, cookie, request header, private disc path, proprietary disc
  byte, or raw achievement definition is stored here.
- The installed RetroArch frontend and SwanStation core remain
  `BINARY-SOURCE-UNMAPPED`; their later negative-claim confidence ceiling is
  Medium.
- Beetle PSX HW, Beetle PSX, and standalone DuckStation remain unavailable in
  the configured local emulation scope. That is not a system-wide absence
  claim.

## Packet contents

- `input-manifest.json` — source pins, selected source-file SHA-256 values,
  public supported-integration snapshot, and collection boundary.
- `source-locations.csv` — candidate load, identification, session, frame,
  media-change, reset, memory-callback, Hardcore, internal-hash, and server
  boundary locations.
- `binary-source-map.csv` — the current integration/binary matrix and its
  source-mapping confidence limits.
- `candidate-searches.csv` — reproducible searches and their disposition as
  leads rather than conclusions.
- `source-review-notes.md` — bounded source observations and explicit
  non-conclusions from the first review pass.
- `integrity-hit-dispositions.csv` — complete source-only disposition of the
  initial integrity-keyword search hits; it distinguishes identification,
  optional image-verification, definition fingerprinting, and unrelated
  mechanisms without making an installed-binary or enforcement claim.
- `consumer-review-notes.md` — review method, key observations, and retained
  uncertainty for the disposition ledger.
- `support-refresh.md` — timestamped current official PlayStation support-list
  refresh, recorded without account state or game content.
- `acquisition-coverage.csv` — requirement-by-requirement R2-C coverage and
  pass/block disposition, including the exact effect of each unavailable input.
- `phase-report.md` — model-assignment record, outcome, scope, confidence
  ceilings, and next eligible work.
- `facts.csv` and `contradictions.csv` — the initial ledger state.

All R2-C artifacts are digested and the inventory/coverage requirements that
do not need unavailable inputs are complete. The independent R2-C pass gate is
blocked only on the enumerated binary/source availability inputs. Static
source work may be reused later with its stated limits, but R2-C has not
issued any binary-behavior or final integrity conclusion.

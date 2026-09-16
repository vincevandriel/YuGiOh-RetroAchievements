# R2-C acquisition and coverage audit

## Execution record

| Field | Value |
|---|---|
| Overlay phase | R2-C — rcheevos and emulator evidence inventory |
| Requested model assignment | GPT-5.6 Terra, High reasoning |
| Actual backend model identifier | Not exposed to this artifact writer; no unsupported model identity is asserted |
| Escalation | None; no compact source-ownership ambiguity survived the bounded review |
| Start of this coverage increment | 2026-09-16T01:46:04Z |
| Coverage observation time | 2026-09-16T02:01:05Z |
| Source/input modes | Pinned local source; configured-scope binary inventory; anonymous official documentation refresh |
| Dynamic activity | None: no emulator, game, authenticated service, or achievement asset was launched, altered, or queried |

## Outcome

**Result: `BLOCKED-INPUT`.**

R2-C has a complete, sealed acquisition packet for all currently available
source and configured-scope binary inventory inputs. It contains a current
official support-list refresh, one inventory row for every supported
PlayStation integration, selected source-file digests, lifecycle candidates,
and a full disposition of the initial integrity-keyword search.

The workstream cannot independently pass because the installed RetroArch
frontend and SwanStation core cannot be mapped to exact source revisions. The
Beetle PSX HW, Beetle PSX, and standalone DuckStation binaries are explicitly
unavailable in the configured local scope. These are input facts, not evidence
that the implementations do not exist elsewhere or that their behavior matches
the reviewed source.

## Gate assessment

| Gate element | Result | Evidence |
|---|---|---|
| Current support list refreshed | PASS | `support-refresh.md` |
| Every current integration represented | PASS | `binary-source-map.csv` |
| Pinned source revisions and selected hashes | PASS | `input-manifest.json` and validation results |
| Candidate and apparent-integrity mechanisms inventoried | PASS | `source-locations.csv` and `integrity-hit-dispositions.csv` |
| Artifacts sealed and prohibited-content scan passed | PASS | `artifacts.sha256` and `validation-results.json` |
| Exact installed-binary/source mapping | BLOCKED-INPUT | `binary-source-map.csv`, COV-008, and COV-009 |
| Independent R2-C pass | BLOCKED-INPUT | `acquisition-coverage.csv`, COV-013 |

## Confidence and handoff boundaries

- Pinned-source observations may be cited as high-confidence, version-bounded
  source observations after R3 completes their call paths and safe fixtures.
- Findings about the installed RetroArch/SwanStation binaries remain capped at
  Medium because exact source mapping is unavailable.
- Beetle PSX HW, Beetle PSX, and standalone DuckStation have no local binary
  evidence in the configured scope. Their static-source discussion must remain
  separate from an observed local-integration claim.
- The support-list refresh is time-sensitive. It is valid only as a dated scope
  selection and must be refreshed before Stage 8 or Stage 11 closure.
- R2-C does not establish any detection, non-detection, enforcement,
  deployment-specific service behavior, or relationship to a loaded reward
  table.

## Next eligible work

The source-only portions of R3 may use this sealed inventory to trace the
recorded call paths and run only generated neutral fixtures. R3 cannot close
an affected binary claim unless COV-008/COV-009 are resolved or the resulting
claim remains explicitly bounded by the listed unavailable/source-unmapped
inputs. R2 as a whole remains paused because R2-A and R2-B are separately
blocked.

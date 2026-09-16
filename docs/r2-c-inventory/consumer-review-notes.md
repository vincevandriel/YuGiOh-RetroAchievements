# R2-C bounded integrity-candidate consumer review

**Observation time:** 2026-09-16T01:46:04Z
**Scope:** pinned source only; no game emulator authenticated service or
achievement asset was launched modified or queried.

## Method

The initial keyword search, `R2C-SEARCH-007`, returned 25 source files. Each
file was assigned to one bounded consumer category in
`integrity-hit-dispositions.csv`. A category records the concrete reviewed
consumer and its narrow relation to the target question. It does not convert a
keyword hit into proof that the mechanism executes for the target, is enabled,
is an enforcement mechanism, or exists in a released binary.

The review does not retain raw achievement definitions, request-validation
material, private-media data, or test instructions for modified target media.

## Material dispositions

- The rcheevos `rc_runtime_checksum` call sites reviewed here operate on
  serialized runtime asset definitions while runtime objects are loaded or
  reused. They are therefore kept separate from emulated-memory, disc-sector,
  and loaded-reward-table questions.
- The normal PlayStation identifier remains a media-identification candidate.
  The existing source observation is preserved, but a generated non-target
  fixture suite is still required to establish its observable input boundary.
- DuckStation source exposes an optional image-verification and Redump lookup
  UI path. It is materially relevant as a separate integrity-adjacent feature,
  but the source evidence does not show that it is part of a RetroAchievements
  session, automatically invoked, selected by a user, successful, or present
  in an installed binary.
- The remaining DuckStation candidates concern memory-card protocol checksums,
  debugger packet framing, or GPU cache accounting. Those are separate
  subsystems in the reviewed files and are not treated as target-media or
  reward-table consumers.
- Reviewed RAWeb candidates are request, award, session-warning, and authoring
  action boundaries. The pinned-action review found no local emulator-media
  reader in those files. It cannot characterize the deployed service or
  unreviewed service code.

## Retained uncertainty

R2-C remains incomplete. This increment has not yet performed the planned
acquisition/coverage audit, source-to-binary mapping, generated fixture work,
or the R3 caller-and-consumer trace. It issues no conclusion about detection,
non-detection, enforcement, current service deployment, or actual loaded
reward/probability values.

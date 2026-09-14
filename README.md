# Yu-Gi-Oh! Forbidden Memories RetroAchievements Integrity Audit

This repository is the evidence workspace for a defensive reverse-engineering
audit of **Yu-Gi-Oh! Forbidden Memories** (PlayStation, NTSC-U,
`SLUS_014.11`) and its RetroAchievements/rcheevos integration.

The audit must answer four questions:

1. Which executable routines load and interpret the duel-reward data in
   `DATA/WA_MRG.MRG`?
2. Does the current RetroAchievements set read, validate, or otherwise depend
   on the resident reward tables or nearby RAM?
3. Do rcheevos and currently supported PlayStation emulators perform any
   additional integrity check that would detect changes outside the boot
   executable or changes to runtime-loaded reward data?
4. Can every answer be reproduced from pinned sources and auditable evidence?

## Current status

**Stages 0–3 complete; paused before Stage 4.** The exact static graph now
identifies the opponent-record loader, asynchronous three-sector read,
deck/rank/reward consumers, tier decision, selected-card path, inventory/history
mutation, and save inclusion. The bounded stock-code review found no
game-native record-content validation, at Medium confidence pending runtime
corroboration. No claim about RetroAchievements or emulator integrity behavior
is established until it passes the later gates and separate final audit.

## Start here

- [Investigation Plan](docs/INVESTIGATION_PLAN.md) — ordered stages, exact
  procedures, deliverables, acceptance gates, and final audit.
- [Remainder Execution Plan](docs/REMAINDER_EXECUTION_PLAN.md) — six bounded
  execution phases mapping unfinished Stages 4–11 to cost-aware model and
  reasoning assignments.
- [Model and Reasoning Allocation Audit](docs/MODEL_REASONING_AUDIT.md) — review
  of the proposed Terra/Sol ladder, escalation rules, and credit controls.
- [Evidence Standard](docs/EVIDENCE_STANDARD.md) — fact IDs, confidence rules,
  contradiction handling, address notation, and repository rules.
- [Preliminary Leads](docs/PRELIMINARY_LEADS.md) — source-grounded hypotheses
  and candidate addresses for the first executor to confirm.
- [Pinned Sources](sources.lock.json) — repository revisions used to construct
  the plan.
- [Evidence Directory Contract](evidence/README.md) — where each stage writes
  its public evidence.
- [Stage 0 Charter](evidence/stage-00-charter/README.md) — passed scope, safety,
  privacy, and handling gate.
- [Stage 1 Provenance](evidence/stage-01-provenance/README.md) — passed target,
  source, emulator, tool, and live-state identity gate.

## Safety boundary

This is an integrity and compatibility audit. It does **not** develop or test
bypasses, concealment, anti-cheat evasion, modified-emulator behavior, or
instructions for keeping altered game files undetected. Controlled tests are
limited to generated synthetic disc fixtures, unmodified stock gameplay with
RetroAchievements disabled where debugging is required, and offline analysis
of achievement logic.

Do not commit disc images, extracted game files, executable bytes, MRG bytes,
save states, credentials, API tokens, request headers, or raw memory dumps.
Derived hashes, addresses, call graphs, compact trace rows, and scripts that do
not contain copyrighted game data are allowed.

## Canonical game record at planning time

- RetroAchievements game ID: `11388`
- Publicly registered PlayStation hash: `b181396315dc9dd3656d5910ea65239b`
- Public page count observed on 2026-09-13: 216 core achievements
- Matching-decompilation reference SHA-1 for `SLUS_014.11`:
  `84747e64f6da8e764206ec203e489acf8c9dcf7d`

These values are inputs to verify, not substitutes for verification. The live
set and supported-emulator list are time-sensitive and must be refreshed at the
start of execution and again before the final audit.

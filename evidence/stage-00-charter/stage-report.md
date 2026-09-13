# Stage 0 — Scope, safety, and handling charter

## Gate

- Result: `PASS`
- Executor: Codex, highest available reasoning
- Started UTC: 2026-09-13T21:31:33Z
- Completed UTC: 2026-09-13T21:33:45Z
- Planning baseline revision: `6d40a77166c8906afa46913cc0cc648da7aac153`

## Objective

Freeze the investigation's target, runtime profiles, publication boundary,
prohibited actions, private-data handling, and stop conditions before any
private game input or authenticated RetroAchievements response is handled.

## Inputs

- `docs/INVESTIGATION_PLAN.md`
- `docs/EVIDENCE_STANDARD.md`
- repository `.gitignore`
- planning-time official supported-emulator list
- the clean planning baseline commit

No private game input, credential, authenticated response, emulator process, or
save file was opened during this stage.

## Procedure performed

1. Created a machine-readable scope for NTSC-U `SLUS_014.11`, game ID 11388,
   scoped reward data, rcheevos, and current officially supported PlayStation
   integrations.
2. Defined `STOCK_OFFLINE_DEBUG`, `STOCK_RA_OBSERVE`, and
   `SYNTHETIC_HASH_FIXTURE` profiles with explicit allowed and forbidden work.
3. Defined ignored local locations for private inputs and raw evidence, using
   placeholders in the tracked example.
4. Defined tracked-path, credential-pattern, and `.gitignore` scan rules.
5. Scanned the clean planning baseline: 14 tracked files, zero prohibited-path
   hits, zero credential-pattern file hits, and zero pre-existing worktree
   changes.
6. Recorded stop conditions for unexpected RA activity, submission risk,
   unknown/modified target identity, write attempts, credential exposure, or a
   request that would cross into evasion research.

## Results

The scope and safety boundary are explicit and machine-readable. Private paths
are permitted only in ignored local configuration; no private value has been
recorded. The baseline and complete Stage 0 gate scans passed. Artifact hashes
are recorded in `artifacts.sha256` and are reverified before publication.

## Facts added or changed

- `CHARTER-001`: target and integration scope frozen.
- `CHARTER-002`: prohibited-work boundary frozen.
- `CHARTER-003`: planning-baseline scan passed.

## Contradictions and unresolved items

No Stage 0 contradictions are open. The live supported-emulator list and game
metadata are intentionally deferred to Stage 1 because they are time-sensitive.

## Safety and privacy check

- No disc image or extracted game file handled: yes.
- No save/save-state or raw RAM capture handled: yes.
- No RA credential, cookie, or authenticated response handled: yes.
- No emulator or game configuration changed: yes.
- No bypass, concealment, or modified-target experiment performed: yes.

## Reproduction procedures

See `reproduction.md`, procedures `STAGE0-REPRO-001` through
`STAGE0-REPRO-003`.

## Gate checklist

- [x] All required deliverables exist.
- [x] Artifact hashes are recorded and reverified after staging.
- [x] Claims have evidence IDs and confidence ratings.
- [x] No private/copyrighted inputs or credentials are committed.
- [x] Failure conditions were checked.
- [x] Stage 1 prerequisites are defined.

## Reviewer sign-off

Primary executor complete; independent final review is reserved for Stage 11.

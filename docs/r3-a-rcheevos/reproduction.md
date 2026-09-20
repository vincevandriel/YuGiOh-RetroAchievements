# R3-A reproduction

All commands and reviews in this packet are source-only. They must not launch
an emulator, read target-game media, use an authenticated account, or make a
network request to RetroAchievements.

## R3A-REPRO-001 — Reproduce the PS1 hash call graph

1. Verify the rcheevos revision and clean worktree against `input-manifest.json`.
2. Verify SHA-256 for `src/rhash/hash.c` and `src/rhash/hash_disc.c`.
3. Inspect the PlayStation dispatch and `rc_hash_psx` ranges listed in
   `source-locations.csv`.
4. Confirm that the graph distinguishes the ordinary file path from the
   playlist branch and labels only the ordinary source path in its assertion.

## R3A-REPRO-002 — Reproduce the size-boundary prediction

1. Inspect `rc_hash_cd_file` and `rc_hash_psx` at the exact ranges in
   `source-locations.csv`.
2. Confirm that a valid header supplies declared payload size plus header and
   that the selected-file helper bounds its final read by the remaining size.
3. Confirm `synthetic-psx-fixture-spec.md` records A3/A5 as `NOT_RUN` source
   predictions, not observed results.

## R3A-REPRO-003 — Reproduce client load/session topology

1. Verify the selected `src/rc_client.c` digest.
2. Trace initial identification through local hash association, game-set fetch,
   session start, activation, memory-address validation, and runtime activation.
3. Require every configured server callback in the graph to remain a boundary;
   do not record request secrets or infer deployed-service behavior.

## R3A-REPRO-004 — Reproduce rehash-trigger classification

1. Inspect the initial-load, explicit-media-change, reset, progress
   deserialization, frame, and unload ranges in `source-locations.csv`.
2. Confirm that `rehash-triggers.csv` calls a hash operation only where the
   reviewed source reaches one and labels external-client dispatch `UNKNOWN`.
3. Reject any wording that turns a bounded routine observation into a
   whole-program or installed-binary negative claim.

## R3A-REPRO-005 — Reproduce per-frame read-path classification

1. Inspect the memory callback, peek helpers, memref update, frame, and event
   ranges in `source-locations.csv`.
2. Confirm that the report says the runtime memref set is asset-defined and
   currently unknown because R2-B is blocked.
3. Confirm no raw asset definition or target address is stored in this packet.

## R3A-REPRO-006 — Implement and execute fixtures only in a later increment

1. Build the future hash driver in a disposable build directory or clean copied
   source tree; never create object files in the pinned source checkout.
2. Implement exactly the generator isolation and A0-A6 relation contract in
   `synthetic-psx-fixture-spec.md`.
3. Run only generated neutral fixtures with network disabled and no emulator.
4. Require a machine-readable result row and a nonzero failure for every
   relation mismatch, unexpected error, nondeterministic output, or prohibited
   input attempt.
5. Keep results `NOT_RUN` until all preceding requirements are met. Never
   substitute target-game media for a synthetic fixture.

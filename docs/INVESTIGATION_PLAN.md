# Investigation Plan

## Purpose and completion rule

This plan answers, for **Yu-Gi-Oh! Forbidden Memories** NTSC-U
(`SLUS_014.11`) and the current RetroAchievements integration:

1. exactly which executable routines load and interpret the duel-reward data
   in `WA_MRG.MRG`;
2. whether the current core achievement set, leaderboards, or Rich Presence
   read, validate, or otherwise depend on the loaded probability values or
   adjacent RAM;
3. whether rcheevos and currently supported PlayStation emulators perform an
   additional scoped integrity check beyond normal game identification that
   would detect non-executable disc-data changes or runtime-loaded reward
   tables;
4. whether all answers are supported by reproducible, pinned evidence.

Planning is complete when this document is approved. The **investigation is not
complete** until Stages 0–10 have passed and Stage 11 issues an independent
`PASS`. A reproducible `UNKNOWN` is an acceptable factual result, but any
mandatory unresolved question prevents an overall `PASS`.

The public planning snapshot observed game ID `11388`, 216 core achievements,
1220 points, and one registered hash (`b181396315dc9dd3656d5910ea65239b`)
on 2026-09-13.[^game][^hashes] Those are freshness markers, not frozen truths.

## Safety and authorization boundary

This is a defensive integrity and reverse-engineering audit. Every executor
must follow these constraints:

- Do not create, test, explain, or optimize a bypass, concealment technique,
  anti-cheat evasion method, modified emulator, or method for keeping altered
  files undetected.
- Never connect a modified game, executable, runtime table, emulator, or save
  state to RetroAchievements. Do not submit unlocks or leaderboard entries
  during research.
- Dynamic stock-game work must use a legally supplied, hash-identified input.
  If debugging requires tooling inconsistent with Hardcore, remain logged out
  of RA or disable the client before boot.
- Hash-boundary experiments use generated synthetic PlayStation fixtures only;
  they do not modify or redistribute Forbidden Memories.
- Do not commit disc files, extracted executable/data files, raw RAM dumps,
  credentials, tokens, cookies, or authenticated headers.
- Do not infer permission to publish private achievement definitions. Commit
  only normalized addresses, classifications, per-definition digests, counts,
  and small logic excerpts when publication is permitted.
- Stop immediately if an action could award an achievement, submit a score,
  expose a credential, or write to a user-owned disc/save artifact.

RetroAchievements' user rules prohibit memory and file manipulation for
unlocking achievements and prohibit modified emulators.[^rules] That policy is
an ethical boundary for the audit; it is not evidence that a technical check
exists.

## Roles and reasoning levels

Stages 0–10 are designed for a **medium** executor; tasks explicitly marked
`Light` may be delegated to a light executor after all listed inputs exist. The
executor follows the steps and gates literally and escalates ambiguity instead
of improvising a conclusion.

Stage 11 requires a fresh, highest-available-reasoning reviewer who did not
author the principal findings. The reviewer must audit from a clean clone and
must not treat earlier confidence labels as evidence.

## Stage dependency map

```text
Stage 0  Scope and safety charter
   |
Stage 1  Freeze exact inputs and live state
   |-----------------------|
Stage 2  Disc/RAM schema    Stage 5  Capture current RA logic
   |                       |
Stage 3  Static call graph  Stage 6  Exhaustive RA dependency analysis
   |
Stage 4  Stock dynamic confirmation
   |-----------------------|----------------------|
Stage 7  rcheevos audit    Stage 8  emulator audit|
   |-----------------------|----------------------|
                    Stage 9  controlled verification
                             |
                    Stage 10 synthesis
                             |
                    Stage 11 independent final audit
```

Stages 2–4 answer the game-data question. Stages 5–6 answer the achievement-set
question. Stages 7–9 answer the client/emulator integrity question. Stage 10
may start drafting earlier, but it cannot close a conclusion until all upstream
gates pass.

## Required repository outputs

Each stage writes under `evidence/stage-NN-*` according to
`evidence/README.md`. At minimum, the completed repository must contain:

- `input-manifest.json` with private inputs represented only by metadata and
  cryptographic hashes;
- a public-state snapshot and set manifest;
- `address-map.csv` and a disc-to-RAM schema;
- loader, consumer, and award call graphs with instruction-address evidence;
- compact stock-execution traces;
- an achievement/leaderboard/Rich Presence dependency matrix;
- rcheevos and emulator integrity-path call graphs;
- a versioned emulator/core matrix;
- a synthetic-fixture verification report;
- a contradiction ledger;
- a final answer report with confidence per claim;
- an independent final audit report.

All generated artifacts must have SHA-256 values in the stage manifest.

---

# Stage 0 — Freeze scope, safety, and handling rules

**Executor:** Light
**Goal:** Make the boundary machine- and reviewer-visible before handling game
data, authenticated set data, or emulator sessions.

## Inputs

- this plan;
- `docs/EVIDENCE_STANDARD.md`;
- repository `.gitignore`;
- names of private inputs and emulator installations, if available.

## Procedure

1. Create `evidence/stage-00-charter/stage-report.md` from the template.
2. Copy the following scope verbatim into `scope.json`:
   - region/revision: NTSC-U, `SLUS_014.11` only;
   - RA game ID: `11388`, subject to Stage 1 refresh;
   - target data: opponent deck/reward records, rank-adjacent data, chosen-card
     result, inventory/chips, and identified load/consumer routines;
   - target integrations: pinned rcheevos, standalone DuckStation, and each
     PlayStation core currently listed as supported by official RA docs;
   - prohibited work: bypass, concealment, evasion, altered-content RA
     sessions, modified-emulator experiments, and unlock/score submission.
3. Record where private game inputs may be read and where temporary local
   evidence may be written. Private paths stay in a local ignored file; the
   committed manifest uses labels such as `PRIVATE_DISC_A`.
4. Define two runtime profiles:
   - `STOCK_OFFLINE_DEBUG`: unmodified game, RA logged out/disabled, debugger
     and read-only traces allowed;
   - `STOCK_RA_OBSERVE`: unmodified game, exact supported hash, normal emulator,
     no debugger writes, no unlock-targeting actions, observation only.
5. Define `SYNTHETIC_HASH_FIXTURE`: fully generated files bearing no game data.
6. Run a dry secret/prohibited-file scan over the repository and record its
   exact rules and output.
7. Add an explicit stop checklist to the report: unexpected RA login, pending
   unlock, modified input, unknown image identity, or credential in output.

## Outputs

- `scope.json`;
- `private-input-locations.example.json` containing placeholders only;
- `stage-report.md`;
- `scan-rules.json` and dry-run results.

## Acceptance gate

Pass only when scope, profiles, prohibited actions, private-data locations, and
stop conditions are explicit; the dry scan exits zero; and no private input is
tracked by Git.

## Failure/stop conditions

- A private path or credential appears in a tracked file.
- The executor cannot keep a debug session disconnected from RA.
- “Supported emulator” or region scope is left implicit.

**Confidence contribution:** none; this stage controls validity and safety.

---

# Stage 1 — Pin exact inputs, tools, binaries, and live state

**Executor:** Light for collection, Medium for reconciliation
**Goal:** Ensure every later result identifies exactly what was analyzed.

## Inputs

- legally supplied NTSC-U disc image or equivalent private dump;
- local emulator installations to be tested;
- `sources.lock.json`;
- official RA pages and documentation.

## Procedure

### A. Identify private game input

1. Record image format, byte length, modification time, and SHA-256 in a local
   ignored intake record.
2. Read `SYSTEM.CNF` without changing the image. Record its `BOOT` path and
   verify that it resolves to `SLUS_014.11`.
3. Extract `SLUS_014.11` and `WA_MRG.MRG` into an ignored temporary directory.
   Record each file's size and SHA-1/SHA-256 in the public input manifest; do not
   commit either file.
4. Confirm executable marker, header load address, entry point, declared text
   size, and actual extracted size. Recompute the expected matching-decomp SHA-1
   rather than trusting a filename.
5. Recompute the rcheevos PlayStation hash using the pinned source. Compare it
   with the live registered hash list and record exact tool output.
6. If any identity check disagrees, mark the input `REJECTED` and stop Stages
   2–4. Do not coerce addresses from a different revision.

### B. Freeze source and tool versions

1. Re-fetch every repository in `sources.lock.json` and verify that each commit
   exists. Do not silently move a pin.
2. Record compiler, debugger, disassembler, scripting runtime, rcheevos/RATools
   parser, and ISO reader versions.
3. Hash all local helper scripts before use.

### C. Snapshot current RA public state

1. Capture UTC time, game title, game ID, console, achievement count, total
   points, supported hashes, code-note count, and revision history indicators
   exposed by official pages.
2. Save the page URLs and SHA-256 of normalized, non-authenticated snapshots
   where terms permit. Otherwise save only the extracted values plus timestamp.
3. Refresh the official supported-emulator page. At planning time it listed
   Beetle PSX HW, Beetle PSX, SwanStation, and DuckStation for PlayStation, but
   execution must use the current list.[^emulators]

### D. Pin installed emulator artifacts

1. For standalone emulators, record product/version, distribution source,
   executable SHA-256, rcheevos library status (bundled/static/dynamic), and log
   version string.
2. For RetroArch, record frontend executable SHA-256 and version, then record
   each exact core library's filename, SHA-256, core name/version, and source
   revision if discoverable.
3. If a binary cannot be mapped to source, label it `BINARY-SOURCE-UNMAPPED`.
   Negative findings for that binary cannot exceed `Medium` confidence.

## Outputs

- `input-manifest.json` with labels, sizes, hashes, and identities but no private
  paths or bytes;
- `public-state.json`;
- `toolchain.json`;
- `emulator-binaries.csv`;
- `source-verification.json`;
- stage report and fact ledger.

## Acceptance gate

Pass only if the private input is conclusively NTSC-U, the boot executable and
RA hash match the intended revision, every source/tool has an immutable version,
the official live state has a timestamp, and every tested binary has a SHA-256.

## Failure/stop conditions

- Wrong or ambiguous region/revision;
- missing legal input for Stages 2–4;
- live RA hash does not match the computed hash;
- a source revision is unavailable or a tool's provenance is unknown;
- credentials or private bytes enter the repository.

**Confidence ceiling if partially complete:** Low for game-specific addresses;
Medium for source-only rcheevos behavior.

---

# Stage 2 — Prove the WA_MRG disc schema and RAM layout

**Executor:** Medium
**Goal:** Establish where each opponent record and sub-array resides on disc and
in RAM, without yet asserting which stock routine interprets it.

## Inputs

- accepted private inputs from Stage 1;
- ISO9660 extent information;
- preliminary layout leads;
- pinned historical and recent reverse-engineering sources.

## Procedure

1. Record the ISO extent/LBA and byte size of `WA_MRG.MRG`. Verify whether all
   calculations use 2048-byte user-data sectors, not raw 2352-byte sectors.
2. Independently derive candidate opponent-record starts from:
   - ISO extent + sector arithmetic;
   - direct WA user-data offsets;
   - cross-reference of load constants/instructions in the stock executable;
   - the historical scrambler layout.
3. For all 39 opponent IDs, calculate:
   - WA-relative record start and end;
   - absolute LBA start and end;
   - four array starts/ends;
   - the 16-byte gaps;
   - candidate 200-byte rank block and 104-byte tail.
4. Read every candidate 722-entry array as little-endian `u16` values and emit
   only derived statistics: element count, sum, nonzero count, first/last
   nonzero index, and SHA-256 of the array bytes. Do not publish the arrays.
5. Test the lead that each of the four arrays totals 2048. A failed total is a
   contradiction, not permission to discard the record.
6. Confirm record stride by comparing the predicted start with the next record,
   file bounds, and the sector references found in code.
7. Build `address-map.csv` with all coordinate systems and independently
   recompute the CPU-to-RA conversion.
8. Create explicit one-byte and multi-byte overlap test vectors for each start,
   end, and gap. These will drive Stage 6's achievement analysis.
9. Label semantic fields conservatively:
   - byte structure may become `CONFIRMED` from direct data;
   - “deck,” “tier 0,” etc. remain `OBSERVED` until consumer instructions prove
     their purpose;
   - rank/tail data remain `UNKNOWN` until read xrefs are resolved.

## Required assertions

- No record exceeds `WA_MRG.MRG` bounds.
- Each record is exactly `0x1800` bytes if the lead holds.
- Each array is exactly 722 little-endian words (`0x5A4` bytes).
- Array stride is exactly `0x5B4`, leaving `0x10` bytes between arrays.
- RAM range `0x801781D8–0x801799D7` maps to RA
  `0x1781D8–0x1799D7` under the pinned rcheevos PS1 map.[^memory-map]
- Calculated ID-1 WA offset agrees—or a contradiction is opened—with the
  independently developed historical tool.

## Outputs

- `disc-layout.csv`;
- `address-map.csv`;
- `array-statistics.csv`;
- `boundary-tests.json`;
- `schema.svg` or Mermaid source;
- fact and contradiction ledgers;
- stage report.

## Acceptance gate

Pass only if two independent derivations agree on every record boundary,
statistics reconcile for all 39 records, coordinate conversions pass boundary
tests, and every semantic label states its current evidence level.

## Failure/stop conditions

- Any out-of-bounds read;
- raw-sector/user-sector ambiguity;
- unexplained record-stride mismatch;
- publication of copyrighted table contents;
- unresolved off-by-one conversion.

**Confidence on pass:** High for byte layout and addresses; no more than Medium
for semantics pending Stages 3–4.

---

# Stage 3 — Recover the exact static loader and consumer call graph

**Executor:** Medium
**Goal:** Identify the precise stock `SLUS_014.11` routines that locate, load,
interpret, select from, and award data associated with the record.

## Inputs

- exact executable from Stage 1;
- Stage 2 address/disc map;
- matching-decomp configuration;
- MIPS R3000 disassembler/decompiler;
- preliminary routine leads.

## Procedure

### A. Establish executable mapping

1. Parse the PS-X EXE header and create a reproducible file-offset ↔ load-address
   map.
2. Import symbols/function boundaries from the matching decomp only after
   verifying its target SHA-1. Mark imported names as inherited, not proven
   semantics.
3. Export the relevant disassembly with virtual addresses and raw instruction
   words. Keep excerpts minimal and never publish the entire executable.

### B. Find the disc-load path

1. Locate immediate values or constructed values corresponding to:
   `0x1D33`, three sectors/`0x1800`, and destination `0x801781D8`.
2. Resolve all xrefs and data-flow predecessors. Determine whether each value is
   an MRG-relative sector, absolute LBA, byte offset, or runtime file handle
   argument.
3. Start at the candidate `func_800179F4`; enumerate all callers, callees, and
   call sites. Continue into the lowest routine that actually initiates the read.
4. For every function in the path, record:
   - exact start/end address;
   - caller and call-site address;
   - relevant argument registers/stack slots;
   - return/error behavior;
   - sector/byte-count calculation;
   - destination calculation;
   - whether the call is synchronous or requires polling/completion handling.
5. Trace upward to the game-state transition that selects the current opponent
   and enters the duel. Trace downward through any MRG index, CD command, DMA,
   memcpy, or decompression helper.
6. Search for every other writer to the full resident range. Classify
   initialization, reload, overwrite, and false positives.

### C. Find all consumers

1. Search instructions for references to each array base and for loops bounded
   by 722, 1444, 1460, or 2048. Include addresses constructed through `lui` plus
   signed offsets.
2. Analyze candidate `func_80021810` instruction-by-instruction:
   - tier validation/range behavior;
   - base and stride calculation;
   - RNG source and transformation;
   - element width and signedness;
   - accumulation comparison;
   - loop bound;
   - returned card numbering;
   - behavior when totals are below/above 2048.
3. Enumerate every caller of the roll routine. Prove or disprove the “single
   caller” lead.
4. Analyze candidate `func_800218F0` and recover the exact tier decision. Map
   each result byte/flag to rank semantics only after tracing its writers.
5. Analyze candidate `func_80021894` and all its callers. Distinguish duel
   rewards from campaign guarantees, password acquisition, starter cards, or
   any other award path.
6. Track the selected card from roll return to results block, presentation, new
   card ring, trunk/inventory update, and persistent save.
7. Resolve xrefs to all deck/gap/rank/tail bytes. If no xref is found, verify
   whether pointer arithmetic hides the access; do not claim unused from a
   literal search.
8. Search for validation logic: table sums, range checks, checksums, record IDs,
   expected sector contents, retry/failure paths, or code-memory integrity.

### D. Produce call graphs

Create three graphs:

1. **Load graph:** duel/opponent selection → MRG lookup → disc read → resident
   destination;
2. **Interpret graph:** results/rank state → tier calculation → weighted scan;
3. **Award graph:** selected card → result display → inventory/save effect.

Each edge must cite a call/jump address or a proven indirect dispatch entry.
Each node must carry a fact ID and confidence.

## Outputs

- `executable-map.json`;
- `functions.csv`;
- `load-callgraph.mmd` and rendered graph;
- `interpret-callgraph.mmd` and rendered graph;
- `award-callgraph.mmd` and rendered graph;
- `instruction-evidence.md` with narrow address ranges;
- `range-writers.csv` and `range-readers.csv`;
- `native-validation-search.csv`;
- fact/contradiction ledgers and stage report.

## Acceptance gate

Pass only when:

- the exact routine that initiates the record read and every relevant ancestor
  through duel setup are identified by address;
- source sector/index, byte count, destination, and error path are proven;
- every reward-array consumer and every roll caller is enumerated;
- tier selection, weighted loop, selected-card storage, and award path are
  described from stock instructions;
- all writers and potential readers of the resident range are dispositioned;
- game-native integrity/validation searches have reproducible coverage.

## Failure/stop conditions

- using project comments as the sole evidence for a function's purpose;
- unresolved overlay/file mapping;
- a computed address that does not match instruction bytes;
- unexplained indirect calls or resident-range aliases;
- renaming a function before its behavior is established.

**Confidence on pass:** High for static addresses and instruction semantics;
runtime timing remains Medium until Stage 4.

---

# Stage 4 — Confirm timing and data flow in unmodified stock execution

**Executor:** Medium
**Goal:** Corroborate the static graph with read-only traces of ordinary,
unmodified gameplay while disconnected from RetroAchievements.

## Inputs

- exact stock input and accepted executable hash;
- `STOCK_OFFLINE_DEBUG` profile;
- Stage 3 function/address tables;
- debugger or trace emulator with read-only watch/break capability.

## Procedure

1. Prove before boot that RA is logged out or disabled. Capture only the setting
   state—not credentials.
2. Start from a clean boot. Do not load a state made from a different image or
   emulator build.
3. Set execute breakpoints at each proposed load-chain and consumer function.
   Set write watches over the 6144-byte destination and compact read watches for
   the three reward arrays where tooling permits.
4. Enter at least:
   - one story duel;
   - one Free Duel;
   - two different opponents whose record hashes differ;
   - one result in each attainable tier class, using ordinary play or existing
     natural saves without editing memory.
5. On the record write, log timestamp/frame, PC, return address, arguments,
   source sector/file identity, destination, length, and before/after SHA-256 of
   the scoped range. Store hashes and compact event rows, not the raw data.
6. Verify that the resident per-array hashes match the corresponding Stage 2
   disc-array hashes for the selected opponent.
7. On roll entry/exit, log tier argument, RNG input/output if naturally visible,
   loop result/card ID, and call site. Recalculate the outcome offline from the
   private table and recorded roll value. Commit only the arithmetic result and
   table hash.
8. On award entry and result display, log selected-card address/value and the
   relevant inventory byte before/after. Avoid any action intended to unlock a
   particular RA achievement.
9. Continue through the next duel to determine when the record is overwritten
   or invalidated.
10. Exercise read/error paths only when naturally reachable without corrupting
    files. Do not alter sectors to force failures.
11. Compare every observed PC/return address to the Stage 3 graph. Open a
    contradiction for an unmodeled writer, consumer, or call site.

## Outputs

- `trace-events.csv` with compact, non-copyrighted observations;
- `trace-manifest.json`;
- `disc-ram-hash-comparison.csv`;
- `timing-sequence.mmd` and rendered timeline;
- `static-dynamic-reconciliation.csv`;
- fact/contradiction ledgers and stage report.

## Acceptance gate

Pass only if two distinct opponents produce matching disc-to-RAM scoped hashes,
the load and reward call paths hit at the predicted addresses, a naturally
observed reward is independently recomputed, overwrite lifetime is documented,
and no unexplained writer/caller remains.

## Failure/stop conditions

- RA becomes active or a submission is possible;
- the game/emulator input hash differs from Stage 1;
- the debugger mutates memory or code;
- a raw table/memory dump is staged for commit;
- traces contradict static analysis without resolution.

**Confidence on pass:** High for loader, timing, selected consumer path, and
disc-to-RAM identity; unexercised branches must retain lower confidence.

---

# Stage 5 — Acquire and normalize the current RetroAchievements set

**Executor:** Light for acquisition, Medium for parser validation
**Goal:** Obtain a complete, timestamped definition snapshot through a normal,
authorized RA client path and transform it into reviewable local inputs without
publishing credentials or private account data.

## Inputs

- current game ID/hash from Stage 1;
- standard RetroAchievements client/emulator authentication owned by the user;
- pinned rcheevos runtime/API parser;
- official public metadata.

## Important limitation

The public RAWeb extended-game API currently exposes a digest-like `MemAddr`
field rather than the full trigger definition in public metadata; RAWeb source
shows that value being generated from the definition.[^raweb-public] A public
achievement list therefore cannot establish memory-address coverage. Use the
standard authenticated client response or an authorized toolkit export.

## Procedure

1. Refresh game page, hash page, and code-note count immediately before
   acquisition.
2. With the **unmodified supported game only**, let a standard client request
   the game data. Never place a token in a command line, trace, or repository.
   Use the client's credential store or a process-local secret source.
3. Capture the decoded response at the normal client boundary, or use an
   official/authorized toolkit export. Sanitize account identifiers immediately.
   Store the full raw response only in the ignored private evidence directory.
4. Build a committed `set-manifest.json` containing:
   - UTC acquisition time;
   - game ID and game hash;
   - endpoint/client version but no query secret;
   - core achievement IDs/titles/points/badge/status;
   - per-definition MD5 and SHA-256;
   - leaderboard IDs and per-component definition digests;
   - Rich Presence digest;
   - total counts and points;
   - source raw-snapshot SHA-256.
5. Keep unofficial/local achievements in a separate manifest. They must never
   influence conclusions about the current core set.
6. Parse every definition with the pinned rcheevos parser (or RATools version
   mapped to that grammar). Record success, bytes consumed, and unsupported
   constructs. No regex-only parser is acceptable.
7. Reconcile counts against public metadata. Account for retired/unofficial
   assets explicitly; do not make totals fit by silently dropping parse errors.
8. If code-note bodies are lawfully accessible through developer tools, export
   a separate sanitized address/name map and its snapshot hash. Code notes are
   corroboration, not proof of what active assets read.

## Outputs

- `set-manifest.json`;
- `assets.csv` with metadata/digests, not necessarily raw definitions;
- `parse-results.json`;
- `public-private-reconciliation.json`;
- optional `code-notes-map.csv`;
- a local ignored raw snapshot;
- stage report and fact ledger.

## Acceptance gate

Pass only if all current core achievements, all active leaderboards, and Rich
Presence are present; every definition parses without unaccounted trailing data;
counts reconcile with the same live revision; and no secret/account-private
data is tracked.

## Failure/stop conditions

- Definitions are unavailable or incomplete;
- only public definition digests—not definitions—were obtained;
- any parser failure or unknown construct is ignored;
- a token, cookie, header, or private raw response enters Git;
- acquisition uses a modified game or risks an unlock/score submission.

**Confidence ceiling if incomplete:** Unknown for any “does not read” claim.

---

# Stage 6 — Exhaustively classify RA memory dependencies

**Executor:** Light once the parser and maps are validated; Medium for indirect
address review
**Goal:** Determine exactly whether and how each current asset touches reward
tables, adjacent record data, or downstream reward state.

## Inputs

- complete parsed set snapshot from Stage 5;
- Stage 2 address/boundary map;
- Stage 3–4 downstream state map;
- pinned rcheevos grammar and PlayStation memory map.

## Procedure

1. Convert each operand to a normalized access record containing asset ID,
   group/condition index, operand role, address mode, base address, size,
   inclusive byte range, transform, delta/prior state, and pointer context.
2. Include all condition groups, reset/pause conditions, measured values,
   hit-count conditions, alternate groups, leaderboard start/cancel/submit/value
   expressions, and Rich Presence lookups/display conditions.
3. Compute byte overlap against:
   - each reward tier;
   - the whole 6144-byte record;
   - each 16-byte gap;
   - rank/tail region;
   - chosen reward card;
   - opponent/result/rank/RNG variables;
   - trunk/inventory and star-chip state;
   - executable code bytes for the identified routines, if mapped into RAM.
4. Handle multi-byte boundary overlap correctly. For example, a 32-bit read
   beginning two bytes before a tier start overlaps the tier and must be listed.
5. Symbolically model address-affecting constructs such as `AddAddress` and
   `Remember`. Determine the finite reachable range from guards and value
   bounds. If the range cannot be proven, classify the asset `E` (`Indirect
   unresolved`) and block a negative conclusion.
6. For every hit, render the entire logical condition in plain language. State
   whether the scoped address controls triggering, pausing, resetting,
   measuring, leaderboard value, or display only.
7. Apply the dependency taxonomy from `EVIDENCE_STANDARD.md`:
   - `A` direct reward-weight read;
   - `B` same-record adjacent read;
   - `C` downstream derived-reward read;
   - `D` causal-only relationship;
   - `E` unresolved indirect reach;
   - `F` exhaustive no-dependency finding.
8. Test whether any asset performs **validation**, meaning it compares source or
   resident bytes to expected constants/digests/invariants or gates progress on
   them. Simply reading a chosen card, rank, inventory count, or chip total is
   not validation.
9. Cross-check normalized addresses against any code notes. A code-note mismatch
   opens a contradiction; it does not automatically invalidate parsed logic.
10. Optionally instrument rcheevos' read-memory callback during
    `STOCK_RA_OBSERVE` to aggregate addresses requested per frame. This can
    corroborate positive reads, but runtime silence cannot prove absence because
    conditions may not activate in the sampled path.
11. Reparse the snapshot a second way—using a second binding/tool or direct
    rcheevos unit harness—and compare access records by canonical digest.

## Outputs

- `normalized-operands.csv`;
- `asset-address-matrix.csv`;
- `range-overlaps.csv`;
- `indirect-range-analysis.md`;
- `validation-analysis.md`;
- `asset-explanations.md`;
- optional `runtime-read-aggregate.csv`;
- parser cross-check report;
- fact/contradiction ledgers and stage report.

## Acceptance gate

Pass only if every asset is accounted for; every address-bearing operand is
normalized; direct and multi-byte overlaps are exhaustive; every indirect path
is bounded or explicitly unresolved; classifications distinguish reads from
validation and causal effects; and two parser paths agree.

## Failure/stop conditions

- regex or textual substring search is used as the sole parser;
- one asset/alt group/leaderboard component/Rich Presence branch is omitted;
- unresolved pointer reach is classified `F`;
- a downstream read is described as source-table validation;
- the set changes before reporting without rerunning the stage.

**Confidence on pass:** High for the pinned set snapshot; conclusions are stale
if the live set changes.

---

# Stage 7 — Audit rcheevos identification, session, and runtime paths

**Executor:** Medium
**Goal:** Determine what rcheevos hashes, when it identifies/re-identifies a
game, what it binds to the session/submissions, and whether it performs any
additional scoped disc or runtime-data validation.

## Inputs

- pinned rcheevos source and tests;
- pinned RA documentation and RAWeb source;
- Stage 1 game hash and set snapshot;
- synthetic fixture specification from Stage 9.

## Procedure

1. Trace console dispatch to `rc_hash_psx` and document the hash algorithm:
   SYSTEM.CNF lookup, `BOOT` parsing, executable-name normalization, PS-X EXE
   header size handling, and bytes supplied to MD5.[^rcheevos-hash]
2. Enumerate every file/sector read reachable from the normal PS1 hashing path.
   Establish whether `WA_MRG.MRG`, the ISO directory as a whole, track checksum,
   or non-boot files enter the registered hash.
3. Run rcheevos hash unit tests and add generated fixture tests covering:
   - same boot name/content, different unrelated sentinel file;
   - same content, different boot path/name;
   - one changed byte within the declared executable extent;
   - bytes beyond the declared PS-X EXE extent;
   - malformed/truncated headers and fallback behavior.
4. Trace `rc_client` from hash identification through game-data download, start
   session, frame evaluation, media change, achievement award, and leaderboard
   submission. Record exactly where game ID and hash are carried or checked.
5. Enumerate every trigger that rehashes media: initial load, explicit media
   change, reset, state load, or periodic work. Distinguish frontend decisions
   from rcheevos APIs.
6. Search for and disposition code concerning checksums, memory validation,
   executable integrity, modified media, hardcore, validation hashes, security,
   tamper, and anti-cheat. Record false positives and server-response checks.
7. Determine what `rc_client_do_frame` evaluates each frame. Confirm whether it
   reads only addresses requested by active asset logic or performs a generic
   RAM/content checksum.[^how-ra-works]
8. Review session/award request construction in pinned source and corresponding
   RAWeb validation. Do not capture or publish a live token or submit a test
   unlock.
9. Separate documented Hardcore feature enforcement from content integrity.
   Official requirements cover features such as cheats, rewind, slowdown/frame
   advance, and state loading; this alone does not prove disc-table validation.[^hardcore]
10. Write both positive and negative findings with call-path completeness. If a
    server-side behavior cannot be inspected or safely observed, label that
    boundary `UNKNOWN` rather than inferring it from client source.

## Outputs

- `psx-hash-callgraph.mmd`;
- `hash-inputs.csv`;
- `client-session-callgraph.mmd`;
- `rehash-triggers.csv`;
- `per-frame-read-path.md`;
- `integrity-search.csv`;
- `server-boundary.md`;
- hash test results;
- fact/contradiction ledgers and stage report.

## Acceptance gate

Pass only if the exact hash inputs and size rules are proven by source and
generated tests; all normal client lifecycle paths are mapped; rehash triggers
are enumerated; generic runtime integrity behavior is confirmed or explicitly
unresolved; and Hardcore restrictions are not conflated with content checks.

## Failure/stop conditions

- a live unlock/leaderboard submission is generated;
- credentials enter logs;
- a negative conclusion relies only on documentation or search keywords;
- server behavior is asserted from inaccessible implementation;
- a synthetic result is generalized beyond the tested version without source
  support.

**Confidence on pass:** High for pinned open-source client behavior; server-side
closed or deployment-specific behavior may remain Medium/Unknown.

---

# Stage 8 — Audit each supported emulator/core integration

**Executor:** Medium
**Goal:** Determine whether the actual supported emulator paths add disc,
executable, or runtime-table validation beyond normal RA identification.

## Scope selection

Use the Stage 1 refresh of the official supported-emulator page, not the
planning-time list. For each listed PlayStation entry, test every materially
distinct integration:

- standalone DuckStation if listed;
- RetroArch frontend paired with the exact installed Beetle PSX HW core;
- RetroArch + Beetle PSX;
- RetroArch + SwanStation;
- any newly listed supported implementation at execution time.

If one project supplies multiple frontends, audit the frontend that owns the RA
integration and the core callbacks separately.

## Procedure for every matrix row

1. Record exact frontend/core binary hashes, version strings, build channel,
   config profile, and source mapping from Stage 1.
2. Trace how the frontend obtains media bytes and calculates/passes the RA hash.
   Identify whether it calls rcheevos hashing or uses a compatible local
   implementation.
3. Trace system start → game identification → `rc_client_begin_load_game` (or
   equivalent) → per-frame `rc_client_do_frame` → media change → session end.
4. Trace the memory callback and document how RA logical addresses map to PS1
   RAM. Verify the resident-table mapping at both boundaries.
5. Enumerate every other game/disc hash and classify its consumer:
   settings database, save naming, compatibility lookup, cover art, UI,
   optional Redump verification, RA identification, or enforcement.
6. Enumerate read paths after boot. Search for periodic disc checks, sector/file
   checksums, executable-memory verification, loaded-data checks, and core
   integrity checks.
7. Trace media-change behavior. Determine whether a re-identification occurs
   only when the frontend signals a disc change or also periodically.
8. Trace Hardcore enforcement: cheats, rewind, run-ahead, slowdown, frame
   advance, save states, memory inspectors, and core options. Record each as a
   feature restriction, not as content validation unless a separate content
   path exists.
9. For DuckStation, explicitly keep its internal game hash separate from its RA
   MD5. Pinned source currently computes the RA hash from executable name and
   declared executable bytes, while the internal hash additionally includes ISO
   PVD and track length.[^duck-details][^duck-hashes]
10. For RetroArch, identify the exact frontend code that hashes initial media,
    handles disc changes, reads memory, and applies Hardcore restrictions. Then
    determine which behavior, if any, resides inside each core.
11. Run the Stage 9 generated fixture suite through each compatible integration
    with network disabled or a mock client. Compare the observed hash and
    re-identification events with source predictions.
12. Complete one `templates/emulator-matrix.csv` row per frontend/core pair.

## Required mechanism columns

- RA identification hash;
- session hash binding;
- emulator-internal identity hash;
- optional disc verification/scanner;
- Hardcore feature gate;
- game-native check;
- periodic runtime content monitor;
- initial-load trigger;
- media-change trigger;
- reset/state-load trigger;
- scoped detection conclusion;
- binary/source confidence.

## Outputs

- `emulator-matrix.csv`;
- one source call graph per distinct integration;
- `binary-source-map.csv`;
- `memory-callback-map.csv`;
- `feature-restrictions.csv`;
- `other-hashes.csv`;
- `runtime-check-search.csv`;
- stage report and fact/contradiction ledgers.

## Acceptance gate

Pass only if every currently supported PlayStation integration is included or
explicitly marked unavailable; binaries and source are mapped; RA hashes are
separated from internal/optional hashes; load/frame/media-change paths are
traced; every apparent integrity mechanism is classified; and negative claims
meet the evidence standard.

## Failure/stop conditions

- treating “DuckStation” and “SwanStation core” as automatically identical;
- treating an optional Redump scan or internal game ID as RA enforcement;
- claiming binary behavior from an unmapped source branch at High confidence;
- testing modified Forbidden Memories media;
- omitting a newly supported emulator from the live list.

**Confidence on pass:** High for exact source-mapped binaries; Medium maximum for
binary/source-unmapped integrations.

---

# Stage 9 — Controlled verification without altered-game RA sessions

**Executor:** Medium
**Goal:** Empirically verify hash boundaries and event timing using generated
fixtures, and verify stock-game observations without probing evasion.

## Test family A: generated PS1 hash fixtures

Create a minimal ISO9660 test family containing a generated `SYSTEM.CNF`, a
synthetic valid PS-X EXE header/payload, and an unrelated sentinel file. Give
fixtures neutral names and no game-derived bytes.

| Fixture | Difference from baseline | Expected if documented algorithm holds |
|---|---|---|
| `A0` | Baseline | Stable reference hash |
| `A1` | Sentinel file content only | Same RA hash |
| `A2` | Sentinel file size/location only | Same RA hash |
| `A3` | One byte inside declared EXE extent | Different RA hash |
| `A4` | Boot executable name/path only | Different RA hash |
| `A5` | Byte beyond declared EXE extent | Result predicted from exact size/clamp implementation |
| `A6` | Malformed/truncated PS-X EXE | Defined error/fallback, not a guessed hash |

These tests characterize implementation boundaries. Do not translate them into
instructions for modifying the target game.

For each fixture, record whole-image SHA-256, generated source manifest, expected
hash relation, rcheevos result, emulator result, log event timing, and pass/fail.
Commit the generator and generated manifests; commit fixture binaries only if
they are fully synthetic and small enough for normal repository policy.

## Test family B: stock target observations

1. In `STOCK_OFFLINE_DEBUG`, confirm the Stage 4 load/consumer trace on the exact
   unmodified target.
2. In `STOCK_RA_OBSERVE`, if safe and useful, boot the exact unmodified supported
   hash and record identification/session events only. Do not target an unlock,
   submit a leaderboard entry, use a debugger writer, or alter any file.
3. Compare the emulator's displayed/logged RA hash with pinned rcheevos output.
4. Trigger a normal reset and, only if the software's ordinary UI supports it,
   an ordinary media eject/reinsert using the same unmodified image. Record
   whether re-identification occurs. Do not substitute altered media.
5. If a behavior cannot be tested without creating an evasion recipe or risking
   RA state, rely on static evidence and mark dynamic confirmation unavailable.

## Test family C: parser/address regression

Generate synthetic achievement definitions covering:

- exact start/end reads for every scoped range;
- 16/24/32-bit overlap across each boundary;
- `AddAddress` with bounded and unbounded indices;
- delta/prior, remembered, measured, reset/pause, alternate groups;
- leaderboard components and Rich Presence.

Run both Stage 6 parsers and require identical normalized access records. This
proves the classifier can detect the relevant patterns without exposing the
live set definitions.

## Outputs

- `fixtures/` generator and manifests;
- `hash-boundary-results.csv`;
- `event-timing.csv`;
- `stock-observation.md`;
- `parser-regression.json`;
- fact/contradiction ledgers and stage report.

## Acceptance gate

Pass only if generated fixture relations match source-derived predictions across
all available integrations; target observations use only exact unmodified
inputs; parser boundary/indirect cases pass; and every omitted dynamic test has
a safety or availability rationale.

## Failure/stop conditions

- any target-game file is altered;
- any modified content connects to RA;
- a fixture contains target-game bytes;
- a test is framed as remaining undetected rather than characterizing inputs;
- expected and observed results differ without an open contradiction.

**Confidence on pass:** High for tested hash boundaries and event timing;
runtime/server behavior outside safe tests retains its source-derived ceiling.

---

# Stage 10 — Synthesize answers and reproducibility package

**Executor:** Medium
**Goal:** Produce concise answers that preserve distinctions, unknowns, version
boundaries, and supporting evidence.

## Procedure

1. Freeze a release candidate commit. Record its Git commit and all evidence
   manifest hashes.
2. Merge fact ledgers without changing original fact IDs. Resolve duplicates by
   references, not deletion.
3. Produce one answer table per research question.

### Required answer format for Question 1

For each loader/interpreter/award routine:

- stock name (`func_address` if no semantic name is justified);
- exact start/end address and file offset;
- call sites and callers;
- inputs/outputs;
- disc source, destination, size, and timing;
- data region consumed;
- static and dynamic evidence IDs;
- confidence and remaining caveats.

The answer must include separate load, tier-decision, weighted-roll,
selected-card, display, and inventory/save paths.

### Required answer format for Question 2

State separately whether the current snapshot:

- directly reads probability weights (`A`);
- reads other bytes in the loaded record (`B`);
- reads downstream reward state (`C`);
- is only causally affected by normal rewards (`D`);
- contains unresolved indirect reach (`E`);
- contains no scoped dependency after exhaustive parsing (`F`).

List asset IDs/titles and exact addresses for every non-`F` result. State
whether any condition validates expected values or merely observes gameplay.

### Required answer format for Question 3

For rcheevos and each emulator/core, answer each mechanism separately:

- normal RA identification inputs;
- when the hash is computed/recomputed;
- session binding;
- internal emulator hashes and their use;
- optional image verification;
- Hardcore feature restrictions;
- periodic runtime/disc/table integrity checks;
- target game-native checks.

Use the wording “no additional scoped check found in version X under paths Y”
rather than an unbounded “no check exists.”

### Required answer format for Question 4

Publish:

- a reproduction index mapping every conclusion to stage/procedure/artifact;
- source and binary pins;
- hashes for all reports and generated outputs;
- exact confidence rationale;
- open contradictions and accepted unknowns;
- refresh instructions for live set/emulator changes.

4. Write an executive summary that cannot be read as authorization to use
   modified content. Do not include operational alteration or evasion steps.
5. Add a “What this audit does not establish” section covering unreviewed server
   deployment, future versions, unsupported emulators, and any missing binary
   mapping.
6. Run repository scans, internal-link checks, CSV/JSON schema validation,
   deterministic regeneration, and clean-clone reproduction.
7. Hand the release candidate—not a mutable worktree—to Stage 11.

## Outputs

- `REPORT.md`;
- `REPRODUCIBILITY.md`;
- `CLAIMS.csv`;
- `CONTRADICTIONS.csv`;
- `release-manifest.json`;
- generated validation results;
- Stage 11 handoff packet.

## Acceptance gate

Pass only if all four questions have explicit answers or clearly blocking
unknowns; every statement maps to evidence; confidence follows the standard;
live-version boundaries are visible; all validations pass from a clean clone;
and the report contains no bypass/evasion material or prohibited data.

## Failure/stop conditions

- an answer merges source-table validation with downstream observation;
- a negative claim lacks completeness evidence;
- a live set changed after Stage 6;
- an open high-impact contradiction is hidden in prose;
- clean-clone regeneration fails;
- the repository contains private/copyrighted input or credentials.

**Confidence on pass:** Candidate only; final confidence is assigned by Stage 11.

---

# Stage 11 — Independent fail-closed final audit

**Executor:** Highest available reasoning; independent from primary execution
**Goal:** Attempt to falsify the report and issue `PASS` only if the complete
evidence chain survives.

## Independence rules

- Start from a clean clone of the Stage 10 release-candidate commit.
- Do not use the primary executor's uncommitted workspace or conclusions as an
  authority.
- Recompute, do not merely inspect, deterministic artifacts.
- Sample high-risk facts first: hash boundaries, address translation, indirect
  achievement access, loader ownership, binary/source identity, and negative
  integrity claims.

## Audit procedure

1. Verify release commit, signatures if used, repository cleanliness, source
   pins, and every evidence SHA-256.
2. Run prohibited-file and secret scans. Fail on any game binary, raw RAM/save
   artifact, credential, authenticated header, or evasion-oriented material.
3. Refresh the official game page, supported hash list, code-note count, and
   supported emulator list. If the achievement set or supported matrix changed
   since Stages 5–8, return `STALE—RERUN REQUIRED`, not `PASS`.
4. Recompute the target rcheevos hash from the private input in a controlled
   local location and verify the public manifest value.
5. Rebuild the matching-decomp target or otherwise verify executable mapping.
   Randomly sample at least ten file-offset/address translations, including all
   relevant boundaries.
6. Independently derive the ID-1, middle, and ID-39 disc records and all resident
   subranges. Check every inclusive end and multi-byte overlap.
7. Audit the loader graph from bottom up. Verify call instructions, argument
   values, destination, length, and error behavior. Reject a graph supported
   only by comments or dynamic labels.
8. Audit the weighted-roll loop and result/award path instruction-by-instruction.
   Recompute at least three observed roll outcomes from trace facts.
9. Re-run the definition parser and classifier. Reconcile asset totals; inspect
   every `A`, `B`, `C`, and `E` classification; then randomly sample at least 20
   `F` assets and all indirect-address assets.
10. Independently search the raw normalized access set for every scoped byte
    range and boundary-overlap vector. A single unreviewed indirect range blocks
    a negative finding.
11. Rebuild/run the synthetic hash fixture tests with pinned rcheevos and all
    available emulator integrations. Verify that expected relations—not just
    printed hash strings—are asserted.
12. Audit each emulator's initial-load, frame, media-change, reset/state, and
    Hardcore paths. Verify that internal hashes and optional verification have
    not been misclassified as RA enforcement.
13. Trace at least one award/session request construction statically without
    performing a live unlock. Confirm what is known and unknown at the server
    boundary.
14. Review every negative claim and ask:
    - Was the searched code path complete?
    - Does the reviewed source match the tested binary?
    - Could indirection, plugins, core callbacks, or deployment-specific server
      behavior escape the scope?
    - Is the wording bounded by version and path?
15. Review `CONTRADICTIONS.csv`. No high-impact contradiction may be open or
    silently accepted. An accepted unknown must appear in the executive summary
    if it affects one of the four questions.
16. Run the clean-clone reproducibility workflow on a second temporary path.
    Compare generated output digests with the release manifest.
17. Write `FINAL_AUDIT.md` containing checks, exact failures/warnings, sampled
    facts, rerun commands/procedures, and one verdict.

## Verdicts

| Verdict | Meaning |
|---|---|
| `PASS` | All mandatory questions are evidence-backed, current, reproducible, safely scoped, and free of material contradiction. |
| `FAIL` | A claim is wrong, evidence/reproduction fails, scope/safety is breached, or a mandatory path was omitted. |
| `STALE—RERUN REQUIRED` | The live set, supported hashes, supported emulators, or relevant release changed after analysis. |
| `INCOMPLETE` | A mandatory input or conclusion remains unknown, including unresolved indirect set access or unmapped critical binary behavior. |

## Automatic non-PASS conditions

- exact NTSC-U input identity is not proven;
- the precise loader/read initiator is not identified;
- weighted-roll/tier/award behavior is based only on third-party comments;
- current complete achievement/leaderboard/Rich Presence definitions are absent;
- any indirect address path remains unbounded while a no-dependency claim is
  made;
- an emulator binary is asserted at High confidence without source mapping;
- a negative integrity claim lacks complete lifecycle coverage;
- live state changed and dependent stages were not rerun;
- an open material contradiction exists;
- clean-clone regeneration differs;
- private/copyrighted/credential data is tracked;
- any procedure tests, teaches, or facilitates bypass, concealment, or evasion.

Stage 11 has no partial-pass option. It may preserve strong individual findings
while returning `INCOMPLETE`, but the overall report cannot call the
investigation complete.

---

# Executor checklists by research question

## Q1: SLUS routines and WA_MRG reward data

- [ ] Exact input and executable hash proven.
- [ ] `WA_MRG.MRG` extent and sector unit proven.
- [ ] All 39 record boundaries independently derived.
- [ ] Resident range and subranges proven.
- [ ] Exact load initiator, ancestors, arguments, destination, size, timing, and
      error path documented.
- [ ] Every record writer and reader dispositioned.
- [ ] Tier decision and weighted scan recovered from instructions.
- [ ] All roll and award callers enumerated.
- [ ] Selected-card/display/inventory/save path documented.
- [ ] Static findings corroborated by stock-only traces.
- [ ] Native integrity/validation search complete.

## Q2: Current RA set dependency

- [ ] Snapshot timestamp and raw digest recorded.
- [ ] Core achievements, active leaderboards, and Rich Presence complete.
- [ ] Counts and points reconcile with public state.
- [ ] Every definition parses using formal grammar.
- [ ] All direct/multi-byte accesses normalized.
- [ ] All indirect accesses bounded or unresolved.
- [ ] Every asset assigned `A`–`F`.
- [ ] Reads, validation, and causal effect stated separately.
- [ ] Code-note comparison complete.
- [ ] Second parser agrees.
- [ ] Snapshot refreshed before final audit.

## Q3: Additional client/emulator integrity checks

- [ ] rcheevos PS1 hash inputs and size behavior proven.
- [ ] Synthetic fixture relations pass.
- [ ] Session/load/change-media/award paths traced.
- [ ] Per-frame runtime read behavior traced.
- [ ] Supported-emulator list refreshed.
- [ ] Every frontend/core binary hashed and mapped to source.
- [ ] Emulator internal hashes classified by consumer.
- [ ] Optional image verification separated from enforcement.
- [ ] Hardcore restrictions separated from content validation.
- [ ] Game-native checks included.
- [ ] Every negative claim is version/path bounded.
- [ ] Server-side unknowns are explicit.

## Q4: Evidence and reproduction

- [ ] Every claim has fact ID, state, confidence, and source.
- [ ] Paths have line ranges or executable addresses.
- [ ] Live observations have timestamps.
- [ ] Contradictions are visible and resolved.
- [ ] All artifacts have SHA-256.
- [ ] Gate scripts fail closed.
- [ ] Clean-clone regeneration passes.
- [ ] Repository scan passes.
- [ ] Independent Stage 11 verdict is `PASS`.

## Sources

[^game]: [RetroAchievements — Yu-Gi-Oh! Forbidden Memories, game 11388](https://retroachievements.org/game/11388)
[^hashes]: [RetroAchievements — supported hashes for game 11388](https://retroachievements.org/game/11388/hashes)
[^rules]: [RetroAchievements — global leaderboard and achievement-hunting rules](https://docs.retroachievements.org/guidelines/users/global-leaderboard-and-achievement-hunting-rules.html)
[^emulators]: [RetroAchievements — emulator support and issues](https://docs.retroachievements.org/general/emulator-support-and-issues.html)
[^memory-map]: [rcheevos PlayStation memory map at pinned commit](https://github.com/RetroAchievements/rcheevos/blob/c28462eafdbeb881a1d442754dd17aae5c4ab834/src/rcheevos/consoleinfo.c#L805-L812)
[^raweb-public]: [RAWeb public extended-game API transformation at pinned commit](https://github.com/RetroAchievements/RAWeb/blob/56cd88e57c6dc6994e130a918e3967f9b74e9eb9/public/API/API_GetGameExtended.php#L94-L126)
[^rcheevos-hash]: [rcheevos PlayStation hash implementation at pinned commit](https://github.com/RetroAchievements/rcheevos/blob/c28462eafdbeb881a1d442754dd17aae5c4ab834/src/rhash/hash_disc.c#L866-L978)
[^how-ra-works]: [RetroAchievements — how RetroAchievements works](https://docs.retroachievements.org/general/how-ra-works.html)
[^hardcore]: [RetroAchievements — Hardcore compliance requirements](https://docs.retroachievements.org/general/hardcore-compliance-requirements.html)
[^duck-details]: [DuckStation game-details and RA-hash dispatch at pinned commit](https://github.com/stenzek/duckstation/blob/96268ab66aa60c434c512bba19d45c75fa7a1b36/src/core/system.cpp#L678-L740)
[^duck-hashes]: [DuckStation internal and RA hash implementations at pinned commit](https://github.com/stenzek/duckstation/blob/96268ab66aa60c434c512bba19d45c75fa7a1b36/src/core/system.cpp#L892-L928)

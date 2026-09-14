# Remainder Execution Plan

## Status and relationship to the canonical plan

This document is the execution overlay for the unfinished portion of the
Forbidden Memories RetroAchievements integrity audit. It does not renumber,
replace, or reopen the canonical evidence stages in
`docs/INVESTIGATION_PLAN.md`.

- Canonical Stages 0–3 are complete at repository commit
  `78c99578d5ddb7ed8317a400dda9cf4b4a79943b`.
- Canonical Stage 4 has not started.
- The six phases below organize canonical Stages 4–11 into bounded work units
  with model, reasoning, escalation, and stop rules.
- A phase passes only when its machine-checkable gate passes. Token expenditure,
  elapsed time, or a persuasive narrative cannot substitute for the gate.

The integrity-only safety boundary in the canonical plan remains controlling.
No phase may develop or test bypasses, concealment, anti-cheat evasion,
modified-emulator behavior, or target-game alterations intended to avoid
detection.

## Model-use policy

Use the least expensive assignment that can reliably meet the evidence gate:

1. **Terra Medium** for checkpoint validation, inventories, manifest work,
   deterministic regeneration, and tightly specified collection.
2. **Terra High** for tool-heavy investigation, source tracing, parser or test
   implementation, dynamic trace orchestration, and bounded technical analysis.
3. **Sol High** for reconciling different evidence types, reviewing ambiguous
   indirection, evaluating negative claims, and assigning confidence.
4. **Sol XHigh** for one compact integration review and the independent final
   audit. It must receive a bounded handoff packet rather than the entire mutable
   research workspace.
5. **Sol Max is escalation-only.** It may be used on a compact exception packet
   when all necessary evidence exists but a material ambiguity survives the Sol
   XHigh audit. It must not be used to compensate for missing inputs, stale live
   data, a failing parser, an unmapped binary, or an incomplete trace.

Do not promote an entire phase because one item is hard. Create an exception
packet containing the claim, exact evidence, competing interpretations,
contradiction IDs, and the decision required; escalate only that packet.

## Phase dependency map

```text
R1  Resume checkpoint and readiness gate                 Terra Medium
 |
 +---------------------------+---------------------------+
 |                           |                           |
R2-A Stock trace         R2-B RA snapshot          R2-C Client/emulator evidence
 |                           |                           |  Terra High
 +---------------------------+---------------------------+
                             |
R3  Exhaustive deterministic classification and tests   Terra High
                             |
R4  Interpretive reconciliation and bounded findings    Sol High
                             |
R5  Complete integrity model and release candidate      Sol High + XHigh gate
                             |
R6  Independent adversarial final audit                  Sol XHigh
                             |
                   Sol Max only for eligible exceptions
```

R2 workstreams may run independently after R1 passes. R3 may start on an R2
workstream only after that workstream's evidence manifest passes, but R3 cannot
close until all required R2 workstreams are complete or explicitly marked
unavailable. R4–R6 are sequential.

---

# R1 — Resume checkpoint and execution readiness

**Primary assignment:** GPT-5.6 Terra, Medium reasoning  
**Canonical coverage:** preflight for Stages 4–9; no canonical stage is redone  
**Purpose:** prove that the completed checkpoint remains valid and identify
missing prerequisites before expensive investigation begins.

## Inputs

- clean checkout of commit `78c99578d5ddb7ed8317a400dda9cf4b4a79943b`;
- Stage 0–3 manifests, reports, validators, and contradiction ledgers;
- private input labels from Stage 1, resolved only in ignored local records;
- current official RA game/hash/emulator metadata;
- installed emulator/core inventory and available debugging interfaces.

## Procedure

1. Record current commit, branch, upstream, and working-tree state.
2. Run every Stage 0–3 validator from a clean checkout. Compare generated
   artifact digests with committed manifests.
3. Verify that the Stage 1 private input still resolves to the same size and
   cryptographic identity without publishing its path or bytes.
4. Refresh only time-sensitive external facts: RA game/hash state, asset count,
   code-note count if available, supported PlayStation integrations, and source
   availability. A changed value opens a freshness item; it does not invalidate
   unrelated static Stage 2–3 evidence.
5. Inventory the prerequisites for the three R2 workstreams:
   - an RA-disabled stock debugger route for R2-A;
   - a normal authorized client/export route for R2-B;
   - exact frontend/core binaries and source mappings for R2-C.
6. Reconfirm the mutually exclusive runtime profiles:
   `STOCK_OFFLINE_DEBUG` and `STOCK_RA_OBSERVE`. No debugger session may be
   connected to RA.
7. Produce a workstream readiness matrix with values `READY`, `BLOCKED-INPUT`,
   `BLOCKED-SAFETY`, or `STALE-RERUN` and an exact reason for every non-ready
   row.
8. Create bounded phase task lists from outstanding canonical acceptance-gate
   items. Do not repeat a Stage 0–3 task merely because its evidence is complex.

## Outputs

- `resume-manifest.json`;
- `freshness-delta.csv`;
- `workstream-readiness.csv`;
- Stage 0–3 validation results;
- a list of eligible R2 tasks and any blocking inputs.

## Pass gate

Pass only if Stage 0–3 validators still pass, the stock input identity remains
accepted, live deltas are dispositioned, safety profiles are explicit, and each
R2 workstream has a machine-readable readiness status.

## Stop and escalation rules

- A failed Stage 0–3 validator stops dependent work and opens a scoped repair;
  it does not authorize a wholesale redo.
- A changed private-input hash stops game-specific dynamic work.
- A missing credential, debugger, binary, or authorized definition source is an
  input blocker, not a reason to increase reasoning effort.
- Escalate to Terra High only if a checkpoint discrepancy cannot be resolved by
  deterministic regeneration and exact manifest comparison.

---

# R2 — Parallel primary evidence acquisition

**Primary assignment:** GPT-5.6 Terra, High reasoning  
**Canonical coverage:** Stages 4, 5, and the evidence-acquisition portions of
Stages 7–8  
**Purpose:** collect complete, pinned evidence in three independent workstreams
without performing cross-stream interpretation.

## R2-A — Stock dynamic trace

Execute canonical Stage 4 against the exact unmodified input under
`STOCK_OFFLINE_DEBUG`:

1. prove RA is disabled before boot;
2. trace the Stage 3 load, record-write, tier-selection, weighted-roll, award,
   and overwrite-lifetime paths for two distinct opponents;
3. collect compact event rows, addresses, arguments, and scoped hashes only;
4. independently recompute at least one naturally observed reward outcome;
5. open contradictions for every unmodeled writer, caller, alias, or timing
   event.

R2-A passes only when the complete canonical Stage 4 gate passes. Naturally
unreachable branches remain lower-confidence rather than being forced.

## R2-B — Current RA definition snapshot

Execute canonical Stage 5 through an authorized normal client/export path:

1. refresh public counts and supported hash immediately before acquisition;
2. acquire all core achievements, active leaderboards, and Rich Presence;
3. sanitize account identifiers and retain full definitions only in ignored
   private evidence;
4. commit metadata and per-definition digests, not credentials or private raw
   responses;
5. parse every definition with the pinned grammar and reconcile all counts.

R2-B passes only when completeness and parser consumption are proven. Public
definition digests alone do not pass this gate.

## R2-C — rcheevos and emulator evidence inventory

Prepare the source and binary evidence required by canonical Stages 7–8:

1. refresh the official supported PlayStation integration list;
2. record exact rcheevos, RetroArch, emulator, and core source revisions;
3. record installed binary filenames, versions, SHA-256 values, and source
   mappings;
4. extract candidate load, identification, session, frame, media-change,
   Hardcore, memory-callback, and other-hash paths into a review inventory;
5. label every source-unmapped binary so its later confidence ceiling is
   enforced automatically.

R2-C is acquisition only. Search hits and project comments remain leads until
R3 traces their consumers and call paths.

## Shared outputs

- one immutable input/evidence manifest per workstream;
- exact tool and source versions;
- compact trace or source-location inventories;
- fact and contradiction ledgers;
- private-data and prohibited-content scan results.

## Shared pass gate

Each workstream passes independently only when its canonical acquisition gate
passes and all outputs have digests. R2 as a whole passes only when all
mandatory workstreams pass. A workstream that cannot execute is marked
`BLOCKED-INPUT` with the affected final claims identified; completed sibling
workstreams remain valid, but R2 and every dependent final conclusion remain
paused rather than receiving a partial pass.

## Stop and escalation rules

- Stop on RA activation during debugging, input-identity drift, credential
  exposure, modified target content, or an unexplained dynamic write.
- Do not use XHigh to perform captures, enumerate files, or rerun parsers.
- Escalate only an ambiguous trace or source-ownership question to Sol High
  after Terra High has produced a minimal exception packet.

---

# R3 — Exhaustive deterministic classification and controlled verification

**Primary assignment:** GPT-5.6 Terra, High reasoning  
**Optional workers:** Terra Medium for already-scripted enumeration  
**Canonical coverage:** Stage 6, completion of Stages 7–8, and Stage 9  
**Purpose:** convert R2 evidence into exhaustive, machine-checkable coverage and
run only safe stock/synthetic verification.

## Procedure

1. Normalize every address-bearing operand from every current achievement,
   leaderboard component, and Rich Presence branch.
2. Model direct, multi-byte, delta/prior, remembered, measured, alternate-group,
   and address-affecting constructs. Bound every indirect range or classify it
   `E — Indirect unresolved`.
3. Compute overlap with reward arrays, the full resident record, gaps/tail,
   downstream reward state, inventory/chip state, and mapped executable bytes.
4. Run two independent parser paths and compare canonical access-record digests.
5. Complete the rcheevos call graphs for PS1 hashing, client load/session,
   per-frame evaluation, media change, award construction, and rehash triggers.
6. Complete every supported frontend/core matrix row. Separate RA
   identification, session binding, internal identity, optional verification,
   Hardcore restrictions, game-native checks, and periodic runtime monitoring.
7. Generate neutral PS1 fixtures containing no target-game bytes and execute the
   canonical Stage 9 hash-boundary tests offline or against a mock client.
8. Run parser boundary-regression fixtures and require both parser paths to
   agree.
9. Run stock-only observation tests where they are safe; never connect modified
   content to RA and never target an unlock or score submission.
10. Produce explicit coverage totals and false-positive dispositions. A search
    with zero hits is not a negative conclusion until the required lifecycle
    paths and indirect cases are accounted for.

## Outputs

- all canonical Stage 6–9 artifacts;
- `coverage-summary.json` containing expected, parsed, classified, mapped,
  tested, unresolved, and omitted counts;
- `exception-packets/` for ambiguous indirect ranges or call paths;
- deterministic gate output for every matrix and fixture family.

## Pass gate

Pass only when:

- every current asset is accounted for and both parser paths agree;
- every indirect path is bounded or explicitly unresolved;
- every currently supported integration has a completed or unavailable matrix
  row with the proper confidence ceiling;
- source call paths cover initial load, frame evaluation, media change,
  reset/state behavior, session end, and award construction;
- all safe fixture relations match their source-derived predictions;
- omissions have explicit safety or availability rationales;
- no high-impact contradiction is hidden or discarded.

## Stop and escalation rules

- Parser disagreement triggers debugging with Terra High, not XHigh review.
- Missing definitions or source/binary mapping block the affected conclusion;
  they cannot be reasoned away.
- A genuinely ambiguous bounded indirect range, call target, or mechanism
  classification becomes a compact Sol High exception packet.
- Terra XHigh is not the default for this phase. Exhaustiveness comes from
  coverage assertions, second parsers, manifests, and fail-closed gates—not from
  unbounded extra reasoning.

---

# R4 — Interpretive reconciliation and bounded findings

**Primary assignment:** GPT-5.6 Sol, High reasoning  
**Canonical coverage:** reconciliation of Stages 4–9 before Stage 10  
**Purpose:** decide what the evidence establishes, resolve contradictions, and
bound every negative claim by version and reviewed path.

## Inputs

- only passed R2/R3 evidence manifests and compact exception packets;
- fact and contradiction ledgers;
- canonical evidence and confidence standards.

## Procedure

1. Reconcile static Stage 3 behavior with stock Stage 4 traces.
2. Reconcile normalized RA accesses with the game-data and downstream-state
   maps. Distinguish categories A–F and distinguish validation from observation
   or causal effect.
3. Reconcile rcheevos behavior with each frontend/core integration. Keep
   internal hashes, optional verification, Hardcore restrictions, and runtime
   content monitoring separate.
4. Review every negative claim for lifecycle completeness, indirect reach,
   binary/source identity, and version scope.
5. Resolve each contradiction through cited evidence or label it
   `ACCEPTED-UNKNOWN`. Never resolve a missing input by inference.
6. Assign claim state and confidence from the evidence standard, not from model
   certainty.
7. Produce a rerun order for any failed or stale item. Rerun only the affected
   upstream workstream.

## Outputs

- reconciled fact ledger;
- contradiction ledger with no silently dropped entries;
- question-by-question preliminary findings;
- bounded-negative-claim checklist;
- confidence rationale and required reruns.

## Pass gate

Pass only if every material claim maps to evidence; categories A–F are applied
consistently; game-native, client, emulator, and server boundaries remain
separate; no high-impact contradiction is open; and every accepted unknown is
visible in the preliminary answers.

## Stop and escalation rules

- Return failed completeness or freshness issues to the responsible R2/R3
  workstream rather than continuing to synthesize.
- Sol XHigh is allowed only for a compact material exception with two plausible
  interpretations and complete underlying evidence.
- If evidence is missing, the result is `UNKNOWN` or `INCOMPLETE`, not an
  escalation to a larger model.

---

# R5 — Complete integrity model and release candidate

**Drafting assignment:** GPT-5.6 Sol, High reasoning  
**Gate review:** GPT-5.6 Sol, XHigh reasoning, one bounded pass  
**Canonical coverage:** Stage 10  
**Purpose:** create the complete claim model and reproducible release candidate,
then subject the integrated model to one focused high-assurance review.

## Procedure

1. Freeze a candidate commit and exact evidence-manifest set.
2. Produce the canonical `REPORT.md`, `REPRODUCIBILITY.md`, `CLAIMS.csv`,
   `CONTRADICTIONS.csv`, release manifest, and Stage 11 handoff packet.
3. Answer each research question in the canonical required format, including
   routines/addresses, RA categories A–F, per-integration mechanisms,
   confidence, versions, evidence IDs, and remaining unknowns.
4. Make every negative statement bounded: “no additional scoped check found in
   version X under paths Y,” never an unbounded “no check exists.”
5. Include what the audit does not establish, especially closed server
   behavior, future releases, unsupported emulators, and source-unmapped
   binaries.
6. Run deterministic regeneration, schema checks, internal-link checks,
   manifest validation, prohibited-content scans, and clean-clone reproduction.
7. Give the Sol XHigh gate reviewer only the release candidate, claim/evidence
   map, contradiction ledger, coverage summary, and canonical gates. The
   reviewer checks cross-stream consistency and returns `ACCEPT`, `REWORK`, or
   `INCOMPLETE` with exact claim IDs.
8. Apply only evidence-backed corrections, rerun all affected validators, and
   freeze the final Stage 11 candidate.

## Pass gate

Pass only when the canonical Stage 10 gate passes, clean-clone regeneration is
deterministic, the live snapshot is still fresh, and the XHigh integration
review returns `ACCEPT`. `REWORK` routes to the named upstream phase;
`INCOMPLETE` remains visible and cannot be polished into a pass.

## Budget boundary

The XHigh reviewer must not repeat raw source discovery, regenerate all evidence
manually, or expand the scope. Its job is integrated correctness over a compact,
versioned packet. This is the only planned non-final XHigh pass.

---

# R6 — Independent adversarial final audit

**Default assignment:** GPT-5.6 Sol, XHigh reasoning  
**Conditional adjudicator:** GPT-5.6 Sol, Max reasoning  
**Canonical coverage:** Stage 11  
**Purpose:** independently attempt to falsify the release candidate and issue a
fail-closed verdict.

## Independence requirements

1. Use a fresh task/context and a clean clone of the frozen Stage 10 candidate.
2. Do not expose the authoring model's private reasoning or treat its confidence
   labels as evidence.
3. Recompute deterministic artifacts and sample high-risk facts before reading
   the executive conclusion.
4. Preserve the canonical Stage 11 verdicts: `PASS`, `FAIL`,
   `STALE—RERUN REQUIRED`, or `INCOMPLETE`.

## Procedure

Execute all canonical Stage 11 checks, prioritizing:

- target identity and address translations;
- loader, weighted-roll, and award instruction paths;
- every A/B/C/E RA dependency and a random F sample;
- indirect address reach and parser agreement;
- rcheevos and emulator lifecycle completeness;
- separation of identification, session, internal hashes, optional checks,
  Hardcore restrictions, and runtime monitoring;
- source/binary mapping and confidence ceilings;
- negative claims, server boundaries, freshness, contradictions, privacy, and
  clean-clone reproducibility.

The audit report must identify sampled fact IDs, exact failed checks, rerun
targets, and one overall verdict. There is no partial `PASS`.

## Default pass gate

Sol XHigh may issue `PASS` only if every canonical Stage 11 automatic non-pass
condition is false and all recomputation/sampling succeeds. A missing input,
stale snapshot, unresolved critical indirection, open material contradiction,
or unmapped critical binary yields the appropriate non-pass verdict.

## Sol Max eligibility gate

Use Sol Max only if **all** of the following are true:

1. the XHigh audit completed every required check;
2. all necessary evidence is present and current;
3. deterministic tests pass;
4. exactly identified material claims still have two or more plausible
   interpretations;
5. the ambiguity could change the overall verdict;
6. a compact adjudication packet can be created without the full mutable
   workspace.

Sol Max receives only that packet and may decide the disputed interpretation.
It may not waive a failed gate, manufacture missing evidence, or convert an
unknown into a factual finding. If these eligibility conditions are not met,
do not spend Max reasoning; return the correct non-pass verdict or rerun the
named upstream phase.

---

# Phase completion record

For every phase, record:

- model and reasoning effort actually used;
- why any escalation was triggered;
- source/input versions and hashes;
- start/end timestamps;
- expected and actual gate results;
- artifacts and SHA-256 values;
- contradiction IDs opened/resolved;
- omissions and confidence ceilings;
- next eligible phase.

A phase report that omits its model/effort or escalation reason fails the
resource-accounting portion of its gate.

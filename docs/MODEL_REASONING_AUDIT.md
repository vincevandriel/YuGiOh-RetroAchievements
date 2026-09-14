# Model and Reasoning Allocation Audit

## Verdict

The proposed ladder is directionally correct but over-provisions reasoning in
its third and sixth stages and leaves “main technical investigation” too broad
to gate reliably. Adopt the six-phase overlay in
`docs/REMAINDER_EXECUTION_PLAN.md` with two changes:

1. run exhaustive bounded verification on Terra High with deterministic
   coverage gates, not Terra XHigh by default;
2. run the independent final audit on Sol XHigh by default and reserve Sol Max
   for a narrowly eligible adjudication packet.

This preserves high assurance while preventing large models from repeatedly
reading, enumerating, or regenerating evidence that scripts and manifests can
verify more reliably.

## Official guidance used

OpenAI currently describes GPT-5.6 Terra as the efficiency-oriented option for
exploration, read-heavy scans, large-file review, and supporting-document work,
while GPT-5.6 Sol (`gpt-5.6`) is the stronger starting point for demanding,
ambiguous, multi-step work involving planning, tools, validation, and
follow-through.[^codex-model-choice] The same Codex guidance describes Medium
as a balanced default, High as appropriate for complex logic, assumptions, and
edge cases, and XHigh/Max as levels for especially demanding reasoning; it also
states that higher effort increases response time and token use.[^codex-effort]

The individual model pages likewise characterize Terra as balancing
intelligence and cost and Sol as the flagship for complex professional work;
both support the reasoning levels used by this plan.[^terra][^sol] These public
descriptions support the relative allocation. They do not establish an exact
Codex-app credit multiplier for this account.

## Proposal-by-proposal assessment

| Proposed assignment | Audit result | Revised use |
|---|---|---|
| Terra Medium — evidence freeze/baseline | Appropriate, but the original baseline is already complete | Use for resume validation, freshness, and readiness only; do not redo canonical Stages 0–3 |
| Terra High — main technical investigation | Appropriate model, insufficiently bounded phase | Split into stock trace, current RA snapshot, and client/emulator evidence workstreams with independent gates |
| Terra XHigh — exhaustive bounded verification | Excessive as a default | Use Terra High plus deterministic validators, a second parser, coverage totals, and synthetic fixtures; escalate only ambiguous exceptions to Sol High |
| Sol High — interpretive reconciliation | Appropriate | Keep for contradiction resolution, confidence, dependency meaning, and bounded negative claims |
| Sol XHigh — complete integrity model | Justified only as a focused gate | Draft with Sol High; perform one Sol XHigh integration review over a compact release-candidate packet |
| Sol Max — adversarial final audit | Excessive as an unconditional full-repository pass | Default to an independent Sol XHigh audit; use Max only when complete evidence leaves a verdict-changing ambiguity |

## Why the revised allocation is sufficient

### Terra Medium is sufficient for R1

R1 is dominated by exact hashes, validator exit codes, manifest comparison,
freshness checks, and readiness classification. Higher reasoning cannot repair a
missing input or make a failed digest pass. The gate is deterministic and any
discrepancy has an explicit escalation path.

### Terra High is sufficient for R2 and R3

These phases are technically demanding, but most difficulty comes from careful
tool use and completeness:

- dynamic breakpoint/watchpoint orchestration;
- source and binary call-path tracing;
- formal parsing and symbolic address bounds;
- complete matrix enumeration;
- synthetic fixture implementation;
- reproducible manifests and tests.

High reasoning is warranted because call graphs, indirect addressing, and
cross-version ownership require sustained logic. XHigh across the full phase is
not the best assurance mechanism. Exhaustiveness is established by explicit
expected counts, two independent parsers, lifecycle coverage, matrix rows,
fixture assertions, false-positive disposition, and nonzero exits on omissions.

### Sol High is appropriate for R4

R4 contains the first deliberately interpretive work: deciding whether an RA
asset directly reads a source table, reads downstream state, is only causally
affected, or validates expected content; and deciding whether an emulator hash
is identification, internal identity, optional verification, or enforcement.
Sol High is appropriate because mistakes here can merge mechanisms that must
remain separate even when all addresses and call paths are correct.

### One bounded Sol XHigh integration review is justified in R5

The full integrity model combines game-native behavior, live set definitions,
rcheevos, several frontend/core paths, dynamic traces, synthetic fixtures,
confidence ceilings, and closed server boundaries. A focused XHigh review is
justified to find cross-stream inconsistencies. It should review the compact
claim/evidence model, not redo raw evidence acquisition.

### Sol XHigh is the correct default for R6

The final audit is the hardest planned task and warrants XHigh. Its reliability
comes from independence, a clean clone, fail-closed verdicts, recomputation,
high-risk sampling, and explicit automatic non-pass conditions. Max reasoning
is not automatically more accurate when a task has missing evidence, broad tool
access, or weak stopping criteria; it can instead spend more time searching
without changing what can be proven.

Max therefore has a strict eligibility gate. It is useful only to adjudicate a
small, fully evidenced, verdict-changing ambiguity that survives the XHigh
audit. It is not a recovery mode for stale or incomplete work.

## Credit-control rules

1. **Do not reread completed stages by default.** Use their manifests and read
   the exact supporting artifact only when a current claim requires it.
2. **Keep context packets bounded.** Each phase receives required manifests,
   maps, exception packets, and the relevant canonical procedure—not every raw
   source tree and prior transcript.
3. **Use code for enumeration.** Expected counts, address overlaps, hashes,
   parser agreement, matrix completeness, and manifest verification must be
   asserted mechanically.
4. **Escalate exceptions only.** Promotion applies to a named claim or call path,
   not to all work in a phase.
5. **Do not spend reasoning on unavailable facts.** Missing definitions,
   credentials, exact binaries, or safe runtime access produce a blocker or
   confidence ceiling.
6. **Use freshness deltas.** When live state changes, rerun only dependent
   analyses instead of repeating stable binary reverse engineering.
7. **Separate authoring from review.** A reviewer receives a frozen candidate
   and cannot silently edit evidence while auditing it.
8. **Stop on a decisive non-pass condition.** Once the overall verdict is
   necessarily `INCOMPLETE`, `FAIL`, or `STALE—RERUN REQUIRED`, finish recording
   the cause and rerun target; do not continue an expensive audit merely to
   accumulate observations.

## Accuracy safeguards independent of model size

- exact input and binary hashes;
- immutable source pins;
- coordinate-system labels for every address;
- two independent derivations or parsers where a negative conclusion depends
  on completeness;
- stock-only dynamic corroboration;
- synthetic fixtures rather than altered target content;
- complete asset and emulator matrices;
- explicit confidence ceilings;
- contradiction preservation;
- clean-clone reproduction;
- an independent final reviewer with fail-closed verdicts.

These controls are more important than raising every phase by one reasoning
level. A stronger model reviews the few places requiring judgment; machines and
bounded procedures establish completeness everywhere else.

## Usage-accounting limitation

Exact Codex-app credit consumption per model and reasoning effort is not assumed
here. Public API token prices and Codex subscription/workspace usage credits are
different accounting surfaces and should not be treated as interchangeable
without an account-specific product statement. The plan therefore optimizes
structurally: fewer premium passes, smaller handoff contexts, deterministic
gates, and conditional escalation. Record actual model/effort and any visible
usage delta in each phase report so later assignments can be tuned from this
project's measured consumption.

## Sources

[^codex-model-choice]: [OpenAI — Codex subagents: model choice](https://learn.chatgpt.com/docs/agent-configuration/subagents#model-choice)
[^codex-effort]: [OpenAI — Codex subagents: reasoning effort](https://learn.chatgpt.com/docs/agent-configuration/subagents#reasoning-effort-model_reasoning_effort)
[^terra]: [OpenAI — GPT-5.6 Terra model](https://developers.openai.com/api/docs/models/gpt-5.6-terra)
[^sol]: [OpenAI — GPT-5.6 Sol model](https://developers.openai.com/api/docs/models/gpt-5.6-sol)

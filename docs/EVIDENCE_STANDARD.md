# Evidence Standard

This file defines what counts as evidence for the Forbidden Memories
RetroAchievements integrity audit. Executors must apply it before interpreting
an address, function, achievement condition, emulator behavior, or negative
finding.

## 1. Claim states

Every material statement must have a fact ID and exactly one state:

| State | Meaning |
|---|---|
| `LEAD` | Plausible starting point that has not met the stage gate. |
| `OBSERVED` | Seen in one trace, source, binary, or data sample but not independently corroborated. |
| `CORROBORATED` | Supported by at least two independent evidence types or independent implementations. |
| `CONFIRMED` | Meets the question-specific acceptance gate and survived contradiction review. |
| `DISPROVED` | A reproducible observation contradicts the proposed claim. |
| `UNRESOLVED` | Evidence is insufficient, ambiguous, stale, or internally inconsistent. |

Do not turn the absence of a search hit into a confirmed negative. Negative
claims require the explicit completeness checks described below.

## 2. Confidence ratings

Confidence measures evidence quality, not how persuasive the prose sounds.

| Rating | Required support | Typical ceiling |
|---|---|---|
| `High` | Exact pinned revision or binary; reproducible result; independent corroboration; no open material contradiction. | Final factual finding. |
| `Medium` | Direct evidence from one authoritative source or two weaker sources, with a known untested boundary. | Static-only call-chain result or binary/source mapping that is not exact. |
| `Low` | Historical tool, comment, name-based inference, single informal report, or unverified address. | Preliminary lead only. |
| `Unknown` | Necessary input is unavailable or the evidence conflicts. | No affirmative or negative conclusion. |

An executor may lower confidence for any reason. Raising it requires meeting all
listed prerequisites. A `CONFIRMED` claim normally requires `High` confidence;
if it does not, explain the exception in the fact row.

## 3. Fact ledger

Copy `templates/fact-ledger.csv` into the relevant stage directory. Assign
stable IDs such as `REWARD-LOAD-001`, `RA-DEP-014`, or `EMU-DS-006`.

Each material fact must include:

- the exact claim;
- claim state and confidence;
- source type and pinned source revision or binary SHA-256;
- a path plus line range, executable address range, or trace-event range;
- the reproduction command or procedure ID;
- at least one corroborating fact ID for a `CORROBORATED` or `CONFIRMED`
  claim;
- any contradiction IDs and the resolution;
- the date observed if the evidence is live or version-sensitive.

Use one fact per row. Do not combine a confirmed address with an inferred
purpose in the same fact: the address may be confirmed while the interpretation
remains provisional.

## 4. Source hierarchy

Prefer evidence in this order, while retaining useful lower-level sources:

1. exact bytes from a legally supplied NTSC-U image or executable, identified
   by hashes, plus a reproducible disassembly or debugger trace;
2. pinned first-party implementation source: rcheevos, RetroArch, an emulator,
   RAWeb, or official RetroAchievements documentation;
3. matching-decompilation output checked against the exact executable;
4. independent debugger traces from an unmodified stock game;
5. reverse-engineering projects and historical tools;
6. comments, naming, forum posts, and undocumented claims.

Source comments are hypotheses until the surrounding instructions or runtime
behavior support them. A recent reverse-engineering fork is not independent
corroboration if it imported the same symbols, notes, or generated output.

## 5. Address notation and translation

Every address fact must identify its coordinate system:

- `CPU-KSEG0`: for example `0x8017878C`;
- `PS1-RAM`: physical two-megabyte RAM offset, for example `0x0017878C`;
- `RA`: rcheevos logical address, normally `0x17878C` for that RAM byte;
- `SLUS-FILE`: byte offset in `SLUS_014.11`;
- `WA-USER`: byte offset in the 2048-byte-per-sector user-data stream of
  `WA_MRG.MRG`;
- `DISC-LBA`: absolute data-sector number in the identified image.

For an NTSC-U PS-X EXE loaded at `0x80010000` with a 2048-byte header, the
initial static mapping to verify is:

```text
SLUS-FILE = CPU-KSEG0 - 0x80010000 + 0x800
PS1-RAM   = CPU-KSEG0 & 0x001FFFFF
RA        = PS1-RAM for the main two-megabyte RAM region
```

Do not apply the first formula to overlays or dynamically loaded code without
proving the overlay's file-to-RAM mapping. Record start and inclusive end,
element width, element count, stride, and any alignment gap. Use a small test
vector at both boundaries to detect off-by-one errors.

## 6. Completeness rules for achievement logic

The phrase “the set does not read this data” is allowed only if all of the
following are true for the same timestamped set snapshot:

1. every core achievement definition was acquired and parsed;
2. every active leaderboard definition was acquired and parsed;
3. Rich Presence was acquired and parsed;
4. every operand was parsed with the pinned rcheevos grammar or an equivalent
   parser checked against rcheevos—not with regular expressions alone;
5. direct reads, multi-byte overlaps, `AddAddress`, `Remember`, measured,
   delta/prior, bit fields, and other address-affecting constructs were
   modeled;
6. every indirect range was either bounded or marked `UNRESOLVED`;
7. resident-table, record-adjacent, and downstream-derived addresses were
   tested separately;
8. parser totals reconcile with the snapshot manifest.

If private/authenticated definitions cannot be acquired, the stage result is
`UNRESOLVED`; public API metadata hashes are not a replacement for the
definitions.

## 7. Dependency vocabulary

Classify each achievement, leaderboard, and Rich Presence display using the
strongest applicable category:

| Code | Category | Meaning |
|---|---|---|
| `A` | Direct value | Reads one or more bytes belonging to a reward-weight array. |
| `B` | Record-adjacent | Reads the resident 6144-byte opponent record outside the three reward arrays, including alignment gaps or trailing data. |
| `C` | Derived reward | Reads a value produced downstream of the tables, such as awarded card, result rank, opponent, trunk count, or star-chip result. |
| `D` | Causal only | Can be affected by ordinary reward outcomes but does not read the source record or a proven direct derivative. |
| `E` | Indirect unresolved | Pointer/add-address behavior might reach the scoped ranges and cannot be bounded. |
| `F` | No dependency found | Exhaustive parsed logic has no direct, adjacent, derived, or unresolved access under the stated snapshot. |

“Depends on” must always be qualified with one of these categories. Category
`C` or `D` is not evidence that the set validates source-table integrity.

## 8. Integrity-check vocabulary

Keep these mechanisms separate in the emulator matrix:

1. **RA game identification** — the content used to produce the registered
   game hash;
2. **RA session binding** — the game ID/hash sent or retained when a session
   starts, media changes, or an award is submitted;
3. **emulator internal identity** — a hash used for settings, save names,
   compatibility databases, or UI;
4. **disc verification/scanning** — an optional Redump, checksum, or image
   diagnostic;
5. **Hardcore feature restriction** — disabling cheats, rewind, save-state
   loading, slowdown, or similar features;
6. **game-native check** — code in `SLUS_014.11` that validates loaded data;
7. **runtime content monitor** — repeated validation of disc sectors, loaded
   reward bytes, or executable memory after identification.

Never infer mechanism 7 from mechanisms 2, 3, 4, or 5.

## 9. Negative-claim standard for integrity behavior

For each emulator/core, a high-confidence statement that no additional scoped
check was found requires:

- exact binary SHA-256 and version string;
- a source revision demonstrably corresponding to that binary, or a documented
  reason for a `Medium` confidence ceiling;
- a call graph from game load through identification, session start, per-frame
  runtime evaluation, media change, and award submission;
- searches for disc rehashing, file/sector validation, memory hashing, code
  integrity, and data-table validation, with false-positive dispositions;
- generated synthetic-fixture observations that distinguish executable-only
  hashing from unrelated-file hashing;
- confirmation that optional verification features and emulator-internal game
  hashes are not being confused with RA enforcement.

Dynamic silence alone cannot prove absence. Source review alone cannot prove
that an installed binary behaves like a different revision.

## 10. Contradictions

Write every material disagreement to `contradictions.csv` with:

- contradiction ID;
- fact IDs in conflict;
- whether it concerns bytes, address, semantics, version, or scope;
- the deciding experiment;
- status (`OPEN`, `RESOLVED`, or `ACCEPTED-UNKNOWN`);
- resolution evidence.

No high-impact claim may be `CONFIRMED` while an associated contradiction is
open. Do not silently overwrite an earlier source pin or interpretation; append
the new observation and link the conflict.

## 11. Reproduction records

Each stage report must state:

- host and tool versions;
- source revisions and input hashes;
- exact invocation or numbered GUI procedure;
- expected output and actual output;
- exit code where applicable;
- artifacts produced and SHA-256 hashes;
- departures from the plan.

Scripts used as gates must be deterministic, emit machine-readable output, and
exit nonzero for missing inputs, parse failures, count mismatches, open
high-impact contradictions, or failed assertions. A screenshot may support a
result, but it cannot replace a machine-readable trace when one is available.

## 12. Repository and privacy rules

Allowed public artifacts include source citations, hashes, address maps, call
graphs, disassembly excerpts small enough to be facts rather than replacement
game code, aggregate tables, scripts, and compact trace rows.

Never commit:

- disc images, `SLUS_014.11`, `WA_MRG.MRG`, or extracted copyrighted assets;
- save files, save states, raw RAM dumps, or large binary-derived blobs;
- RetroAchievements credentials, API tokens, cookies, request headers, or
  authenticated response archives containing private account data;
- instructions or tools whose purpose is bypass, concealment, evasion, or
  making altered files appear legitimate.

Before every push, run a secret scan and a filename/content signature scan for
prohibited inputs. If a prohibited artifact was staged, unstage it and record
the incident locally; do not try to “clean” a published secret by merely adding
it to `.gitignore`.

# R3-A neutral PS1 hash-fixture specification

## Purpose and status

This is a **test design only**. No image, cue, executable, hash, or emulator
result was generated in R3-A. A later implementation may characterize the
pinned rcheevos source boundary using only fresh neutral data generated inside
its own output directory. It must never accept a target-game file, byte range,
or path as an input.

The fixture family is intended to test a source-derived relation, not to
produce a recipe for changing any real game or for avoiding detection.

## Non-negotiable generator contract

1. Accept only a deterministic seed, fixed neutral payload sizes, and an empty
   output directory created by the runner.
2. Reject every input path, external file handle, environment-supplied media
   location, and non-empty pre-existing fixture directory.
3. Generate a minimal ISO9660 layout with a neutral `SYSTEM.CNF`, one neutral
   PS-X EXE-style primary file, and one neutral sentinel file. All strings and
   payload bytes are deterministic generator outputs.
4. Record only fixture names, whole-image SHA-256 values, generator revision,
   selected source revision, and relation assertions. Do not commit image
   bytes unless a later repository policy explicitly permits the small,
   independently reviewed synthetic binary artifact.
5. Scan the generated manifest and generator source for prohibited private
   material before any result is committed. Treat a scan hit or nondeterminism
   as a test failure.
6. Run the hash driver against a disposable generated fixture directory using
   the pinned rcheevos source implementation. Do not launch an emulator,
   authenticate, or contact RetroAchievements.

## Fixture family

| Fixture | Sole generated difference from A0 | Source-derived expected relation | Execution status |
|---|---|---|---|
| A0 | Neutral baseline with valid boot entry, valid primary header, and sentinel | Establish reference result | `NOT_RUN` |
| A1 | Sentinel-file content only | Same as A0 | `NOT_RUN` |
| A2 | Sentinel-file size and location only, while selected primary file and locator metadata remain stable | Same as A0 | `NOT_RUN` |
| A3 | One byte strictly within the primary file's header-plus-declared payload extent | Different from A0 | `NOT_RUN` |
| A4 | Primary boot name/path only, with otherwise identical valid selected content | Different from A0 because the normalized executable name is appended before selected bytes | `NOT_RUN` |
| A5 | One byte strictly after the primary file's header-plus-declared payload extent, with all earlier selected bytes and locator metadata stable | Same as A0 under the reviewed bounded-size path | `NOT_RUN` |
| A6a | Readable primary file with invalid header marker | Defined alternate size path; record success/error and resulting relation without pre-asserting a specific digest | `NOT_RUN` |
| A6b | Truncated primary file that cannot supply the header read | Expected error | `NOT_RUN` |

`A6a` and `A6b` intentionally split the canonical malformed/truncated case:
the pinned source treats a readable invalid marker differently from an
insufficient header read. The runner must assert the stated success/error
class, not merely print a digest.

## Relation rationale

For an ordinary non-playlist PlayStation file path, the pinned implementation
opens track one, uses `SYSTEM.CNF`/`BOOT` with a fallback primary name, appends
the selected executable name, then asks `rc_hash_cd_file` to append the chosen
file bytes. With a valid header, its requested byte count is the declared
payload size plus the fixed header. `rc_hash_cd_file` appends no more than that
supplied size and bounds the final partial read by remaining bytes. This is why
A3 and A5 have different predicted relations.

These are source-derived predictions only. Every `NOT_RUN` relation must become
either `PASS`, `FAIL`, or `UNRESOLVED` in the later evidence artifact. A failed
relation opens a contradiction and stops any broader inference.

## Required result schema

Each future result row must include:

- fixture ID and deterministic generator revision;
- fixture whole-image SHA-256 and generated-manifest SHA-256;
- selected rcheevos source revision and hashing-driver build identifier;
- expected relation, observed result class, and asserted relation outcome;
- whether any file reader error occurred;
- explicit statement that no emulator, target media, account session, unlock,
  or leaderboard submission was involved.

The future runner must fail nonzero for nondeterminism, prohibited-content scan
failure, an unexpected hash error, a relation mismatch, or an attempt to read
outside its generated output directory.

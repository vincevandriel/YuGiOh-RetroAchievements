# Evidence directory contract

Create one directory per stage only when that stage begins:

```text
evidence/
  stage-00-charter/
  stage-01-provenance/
  stage-02-disc-layout/
  stage-03-static-re/
  stage-04-runtime-trace/
  stage-05-ra-set/
  stage-06-dependency-map/
  stage-07-rcheevos/
  stage-08-emulators/
  stage-09-controlled-verification/
  stage-10-synthesis/
  stage-11-final-audit/
```

Each stage directory must contain:

- `stage-report.md` — what was attempted, what completed, failures, and gate
  result;
- `facts.csv` — claim-level evidence rows using the repository schema;
- `reproduction.md` — reproducible command or numbered GUI procedures with
  secrets, private paths, and usernames removed;
- `artifacts.sha256` — SHA-256 for every committed evidence artifact in that
  stage;
- `contradictions.csv` — open and resolved conflicts using the shared template;
- `README.md` — a compact index of the stage's files.

Raw captures belong under a local `raw/` child. Every `raw/` directory is
ignored by Git. Commit only sanitized and minimized derivatives. A derivative
must identify its raw source by a local evidence ID and SHA-256; it must not
reveal the private source path.

Do not pre-create empty stage directories. The presence of a numbered stage
directory means execution has started; `gate: PASS` in its report means it is
complete.

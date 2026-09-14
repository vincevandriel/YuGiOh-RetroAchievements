# Stage 3 — exact static loader and consumer graph

Gate: **PASS**

Start with [stage-report.md](stage-report.md), then use:

- `functions.csv` for exact routines, bounds, callers, and roles;
- the three `.mmd` files for load, interpretation, and award graphs;
- `instruction-evidence.md` and `instruction-windows.csv` for narrow stock
  instruction evidence;
- `direct-call-xrefs.csv`, `pointer-xrefs.csv`, and `constant-hits.csv` for
  whole-range search evidence;
- `record-request-contexts.csv` for bounded backward slices at all 21 generic
  request-wrapper call sites;
- `range-readers.csv` and `range-writers.csv` for complete scoped disposition;
- `native-validation-search.csv` for validation and negative-search coverage;
- `facts.csv` and `contradictions.csv` for claim status and conflicts;
- `reproduction.md` for deterministic verification.

This stage does not include emulator execution, RetroAchievements logic, or
runtime tracing. Those remain gated later stages.

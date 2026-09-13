# Stage 0 evidence index

Gate purpose: freeze the audit boundary before handling private or authenticated
inputs.

- `scope.json` — exact target, integration scope, runtime profiles, publication
  boundary, prohibited work, and stop conditions.
- `private-input-locations.example.json` — placeholder-only local configuration
  contract.
- `scan-rules.json` — prohibited tracked paths, secret patterns, and required
  ignore rules.
- `scan-results.json` — planning-baseline dry-scan result.
- `facts.csv` — Stage 0 claim ledger.
- `contradictions.csv` — Stage 0 contradiction ledger; header only at gate.
- `reproduction.md` — reproducible inspection and scan procedures.
- `stage-report.md` — gate record.
- `artifacts.sha256` — generated at gate after all other artifacts stabilize.

No raw/private evidence exists for this stage.

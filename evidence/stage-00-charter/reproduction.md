# Stage 0 reproduction

## STAGE0-REPRO-001 — Inspect the frozen scope

1. Check out the Stage 0 gate commit.
2. Parse `scope.json` with a standards-compliant JSON parser.
3. Confirm that the target, three runtime profiles, publication boundary,
   prohibited work, and stop conditions are present.
4. Confirm that `private-input-locations.example.json` contains placeholders
   only and directs real values into an ignored `private/` location.

Expected result: both JSON documents parse; no private path, credential, or
game-derived byte is present.

## STAGE0-REPRO-002 — Dry repository scan

From the repository root, enumerate tracked paths and compare them
case-insensitively with every `prohibited_tracked_path_patterns` expression in
`scan-rules.json`. Then search tracked text for every
`secret_content_patterns` expression. Finally, verify that every
`required_gitignore_patterns` literal is present in `.gitignore`.

Expected result: zero prohibited-path hits, zero secret-pattern hits, and all
required ignore rules present. Any match is a failure requiring manual review;
the scan must not delete or rewrite a file automatically.

## STAGE0-REPRO-003 — Gate integrity

1. Parse every Stage 0 JSON file.
2. Parse both CSV files and verify that their headers match the shared
   templates.
3. Recompute SHA-256 for every artifact listed in `artifacts.sha256`.
4. Confirm that `contradictions.csv` contains only its header.
5. Confirm that Git has no tracked file matching the prohibited path rules.

Expected result: all parses and hashes succeed, and there are no open
contradictions.

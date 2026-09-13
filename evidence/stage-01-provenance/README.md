# Stage 1 evidence index

Gate purpose: prove exact target identity and freeze source, emulator, tool, and
official-live inputs for subsequent stages.

- `input-manifest.json` — sanitized private-input metadata, ISO extents, file
  hashes, PS-X EXE header, and rcheevos result.
- `public-state.json` — official game/set/hash/code-note/emulator snapshot.
- `source-verification.json` — fetched source pins and default-branch checks.
- `toolchain.json` — exact tools and helper hashes.
- `emulator-binaries.csv` — available and not-discovered integration inventory.
- `facts.csv` — Stage 1 fact ledger.
- `contradictions.csv` — header-only contradiction ledger at the gate.
- `reproduction.md` — six reproducible procedures.
- `stage-report.md` — gate result, limitations, and source links.
- `artifacts.sha256` — generated after all other artifacts stabilize.

The ignored private extraction contains the nine ISO files and private path
metadata. It is neither required nor permitted in the public repository.

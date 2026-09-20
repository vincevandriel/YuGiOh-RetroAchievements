# R3-A per-frame read-path review

## Bounded pinned-source path

In the reviewed pinned `rc_client.c` path, the frontend or embedding caller
first installs a read-memory callback through
`rc_client_set_read_memory_function` (line 5838). The client then uses that
callback through bounded one-to-four-byte peek helpers. Read failures can
invalidate the current processing memory reference and dependent active assets.

For a loaded game that is not waiting for reset, `rc_client_do_frame`:

1. clears pending event state;
2. calls `rc_client_update_memref_values`;
3. updates only the runtime memory-reference lists held by the loaded runtime;
4. evaluates active achievements, eligible leaderboards, and Rich Presence;
5. raises the resulting pending events outside the mutex; and
6. invokes its scheduled-work idle path.

The reviewed source locations are `rc_client.c` lines 5838–6028 and
6424–6457. The lifecycle graph records where pending achievement and
leaderboard events proceed to configured server callbacks; it does not record
request formulae, session material, or a live interaction.

## What is and is not classified

| Question | R3-A result | Reason |
|---|---|---|
| Does the reviewed per-frame path read runtime memrefs? | Observed | `rc_client_update_memref_values` iterates the runtime memref lists and uses the configured reader. |
| Are the current Forbidden Memories addresses known? | Unknown | R2-B's authorized, complete current asset snapshot is blocked. No raw definitions were acquired. |
| Does the reviewed path itself call the PS1 hash generator? | Not observed in reviewed routine | No `rc_hash` call occurs in the bounded `rc_client_do_frame` range. This is not a whole-program absence claim. |
| Does this prove no generic content monitor exists anywhere? | No | R3-A does not elevate a bounded trace into an unbounded negative conclusion. |
| Does this describe an installed frontend/core binary? | No | R2-C records unmapped installed binaries and unavailable integrations. |

## Required later checks

- R2-B must provide an authorized, sanitized complete definition snapshot
  before the runtime memref set can be normalized and classified.
- R3 fixture execution can test only neutral hash relations; it cannot prove
  the current asset set or deployed-server behavior.
- An integration-specific review must retain separate categories for RA
  identification, session binding, internal identity, optional image
  verification, Hardcore restrictions, and any claimed periodic monitor.

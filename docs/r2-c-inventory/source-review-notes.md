# R2-C first bounded source-review pass

**Observation time:** 2026-09-14T23:21:54Z  
**Scope:** pinned source only; no emulator or game was launched.

## Resolved bundled-source provenance item

The selected upstream rcheevos and RetroArch-bundled `rc_client.c` files have
the same SHA-256. Their selected `hash_disc.c` files differ, but the complete
no-index diff contains one hunk only: it removes PS3-specific helpers beginning
at upstream line 1071, after `rc_hash_psx` ends at line 980. The pinned upstream PlayStation
function is lines 928–980. Therefore the selected source files contain the
same PS1 hash-function text at this checkpoint.

This is a source-file observation only. The installed RetroArch executable and
SwanStation core are still source-unmapped, so this does not establish their
released-binary behavior.

## Lifecycle and memory-reader skeleton

| Layer | Observed source path | Bounded observation | Still required |
|---|---|---|---|
| Upstream rcheevos | `rc_client_do_frame` → `rc_client_update_memref_values` → active-achievement, leaderboard, and Rich Presence workers | The frame path updates runtime memory references through its configured memory reader before evaluating active assets. | Determine the complete provenance of configured memory references from the actual set; do not infer a generic content scan is absent from this fragment alone. |
| RetroArch | `rcheevos_load` → `rc_client_begin_identify_and_load_game`; `rcheevos_change_disc` → `rc_client_begin_identify_and_change_media` | The frontend source has explicit initial-load and disc-change entry points. Its first memory read initializes the libretro memory map and replaces the temporary reader with `rcheevos_client_read_memory`. | Trace callers/conditions, source-map the released frontend/core, and compare safe fixture behavior. |
| DuckStation | `System::GetAchievementsHash` → `Achievements::SetGameHash` → load or explicit `begin_change_media_from_hash`; `FrameUpdate` → `rc_client_do_frame` | The source keeps an internal game hash and a separate RA hash path. Its client reads RAM or scratchpad through `ClientReadMemory` after an address-range guard. | Trace all callers and consumers, map a released binary if one becomes available, and test only safe fixtures. |

## Hash implementation observation

Pinned upstream `rc_hash_psx` opens track 1, locates the boot executable from
`SYSTEM.CNF` with a `PSX.EXE` fallback, reads the executable header, includes
the executable name, and supplies the declared PS-X EXE extent plus the
2048-byte header to the hash helper. The planned generated fixture suite is
still required to demonstrate the resulting boundary behavior. This review does
not test altered target media and does not make a runtime-detection claim.

## Integrity-keyword search boundary

The first bounded keyword search found candidate files in all four source
layers. A hit is not evidence of a reward-table, disc-content, or executable
integrity mechanism. Each hit must be traced to a consumer and classified in
the later R3 review. No negative conclusion has been issued from this search.

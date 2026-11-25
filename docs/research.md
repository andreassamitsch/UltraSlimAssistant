# Research plan

## Current baseline (2026-11-25)
Target HW-S800D, reported firmware SAT-MT8532D24WWC-1072.1. The public USB package is an older reference, not a confirmed exact match. Platform name suggests MediaTek MT8532; OS and audio interfaces remain unverified.

Official source: https://www.samsung.com/at/support/model/HW-S800D/EN/

## Phase 1 — Offline inventory
- Obtain original USB ZIP from Samsung; record source, timestamp, archive size and SHA-256.
- Enumerate ZIP members and compressed/uncompressed sizes without extracting.
- Identify package formats from documented metadata. Record factual observations separately from hypotheses.
- Check Samsung's open-source notices for corresponding platform source.

## Phase 2 — Feasibility
- Identify documented audio and voice interfaces; establish whether microphone capture is supported.
- Compare platform architecture with published research on older soundbars; do not assume compatibility.
- Evaluate Home Assistant Assist clients and playback coexistence. Preserve mute/privacy controls.
- No device modification or execution of vendor binaries during offline research.

## Storage policy
Keep archives and extracted files outside Git; do not upload them to LFS, releases, Actions caches or artifacts. Use a disposable runner or local disk. Save only reviewed small metadata reports and original analysis. Public logs must not include secrets or proprietary payloads.

## Open questions
Exact 1072.1 image availability, OS, CPU architecture, audio stack, documented extension mechanism, recovery options, and microphone access.

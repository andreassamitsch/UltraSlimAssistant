# UltraSlimAssistant roadmap

Goal: Home Assistant Assist using the original HW-S800D microphone and playback hardware, while preserving all vendor functionality. Public research repository; no proprietary binaries, private diagnostics or credentials.

## Completed
- [x] Identify target hardware and installed firmware (SAT-MT8532D24WWC-1072.1).
- [x] Reproducible firmware download and inventory; no retained binary.
- [x] MSD metadata and entropy inspection; strong encryption evidence.
- [x] Read-only OCF diagnostics: microphone flag, Alexa and vendor app-update support, Tizen-related package IDs.

## Phase 3 — documented local interfaces
- [x] Review LocalThings source and available device diagnostics for documented capture or app APIs (no supported capture stream found).
- [ ] Inventory supported playback/discovery protocols and development interfaces; source review complete, direct LAN inventory blocked by current read-only tooling.
- Gate: identify a supported, authorized audio-capture interface before building a microphone client.

## Phase 4 — application environment
- [x] Review Samsung open-source portal, model documentation and official Tizen SDK capabilities (portal unavailable; generic native audio API documented).
- [ ] Establish whether a soundbar-specific developer application mechanism exists.
- [x] Decision: no outreach to Samsung. Use publicly available material and existing authorized local interfaces only.
- Gate: confirm supported deployment, permissions, uninstall/recovery before any device installation.

## Phase 5 — audio architecture
- [ ] Establish capture format, microphone permission and mute/indicator behavior.
- [ ] Determine whether documented processed audio and echo cancellation are available.
- [ ] Evaluate playback coexistence and explicit activation.
- Gate: no audio recording until consent, mute behavior and indicators are verified.

## Phase 6 — prototype
- [x] Host-side test with synthetic audio and documented Assist protocol (run 45683705531).
- [ ] Device prototype only if the supported deployment and capture gates pass.
- [ ] Verify playback, HDMI/eARC, updates and rollback.

## Latest evidence
- Device explicitly reports Tizen 8.0; see [platform and SDK findings](findings/2026-11-25-platform-sdk.md).
- Native API candidates identified; supported soundbar deployment remains the primary gate.

## Decision paths
A: supported native application (preferred for integration).
B: documented network audio interface (simpler if available).
C: vendor-supported firmware extension only if documented and recoverable.
D: external voice satellite / Alexa skill fallback if no supported microphone access.

## Boundaries
No flashing, modifications to production settings, authentication bypass, private audio collection, or proprietary firmware redistribution. Public research reports contain only sanitized facts. Automated CI limited to tests and explicit firmware-tool changes; no persistent firmware artifacts.

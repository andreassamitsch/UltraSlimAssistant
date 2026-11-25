# UltraSlimAssistant roadmap

Goal: Home Assistant Assist using the original HW-S800D microphone and playback hardware, while preserving all vendor functionality. Public research repository; no proprietary binaries, private diagnostics or credentials.

## Completed
- [x] Identify target hardware and installed firmware (SAT-MT8532D24WWC-1072.1).
- [x] Reproducible firmware download and inventory; no retained binary.
- [x] MSD metadata and entropy inspection; strong encryption evidence.
- [x] Read-only OCF diagnostics: microphone flag, Alexa and vendor app-update support, Tizen-related package IDs.

## Phase 3 — documented local interfaces
- [ ] Review LocalThings source and available device diagnostics for documented capture or app APIs.
- [ ] Inventory supported playback/discovery protocols and development interfaces; distinguish observed from inferred.
- Gate: identify a supported, authorized audio-capture interface before building a microphone client.

## Phase 4 — application environment
- [ ] Review Samsung open-source portal, model documentation and official Tizen SDK capabilities.
- [ ] Establish whether a soundbar-specific developer application mechanism exists.
- [ ] Request corresponding open-source components and supported SDK information from Samsung (draft available; not sent).
- Gate: confirm supported deployment, permissions, uninstall/recovery before any device installation.

## Phase 5 — audio architecture
- [ ] Establish capture format, microphone permission and mute/indicator behavior.
- [ ] Determine whether documented processed audio and echo cancellation are available.
- [ ] Evaluate playback coexistence and explicit activation.
- Gate: no audio recording until consent, mute behavior and indicators are verified.

## Phase 6 — prototype
- [ ] Host-side test with synthetic audio and documented Assist protocol.
- [ ] Device prototype only if the supported deployment and capture gates pass.
- [ ] Verify playback, HDMI/eARC, updates and rollback.

## Decision paths
A: supported native application (preferred for integration).
B: documented network audio interface (simpler if available).
C: vendor-supported firmware extension only if documented and recoverable.
D: external voice satellite / Alexa skill fallback if no supported microphone access.

## Boundaries
No flashing, modifications to production settings, authentication bypass, private audio collection, or proprietary firmware redistribution. Public research reports contain only sanitized facts. Automated CI limited to tests and explicit firmware-tool changes; no persistent firmware artifacts.

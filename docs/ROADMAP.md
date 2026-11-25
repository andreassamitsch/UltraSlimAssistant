# UltraSlimAssistant roadmap

Goal: Home Assistant Assist using the original HW-S800D microphone and playback hardware, while preserving all vendor functionality. Public research repository; no proprietary binaries, private diagnostics or credentials.

## Completed
- [x] Identify target hardware and installed firmware (SAT-MT8532D24WWC-1072.1).
- [x] Reproducible firmware download and inventory; no retained binary.
- [x] MSD metadata and entropy inspection; strong encryption evidence.
- [x] Read-only OCF diagnostics: microphone flag, Alexa and vendor app-update support, Tizen-related package IDs.

## Phase 3 — documented local interfaces
- [x] Review LocalThings source and available device diagnostics for documented capture or app APIs (no supported capture stream found).
- [x] Bounded 22-port inventory and read-only HTTP/SSDP/mDNS classification completed. Samsung API reports developerMode=0; SDB port refused. Supported developer path remains open. See [service inventory](findings/2026-11-25-service-inventory.md).
- Gate: identify a supported, authorized audio-capture interface before building a microphone client.

## Phase 4 — application environment
- [x] Review Samsung open-source portal, model documentation and official Tizen SDK capabilities (portal unavailable; generic native audio API documented).
- [ ] Establish whether a soundbar-specific developer application mechanism exists. Shared REST API developerMode=0 is not proof of support; TV-only instructions do not establish soundbar compatibility. See [developer mode review](findings/2026-11-25-developer-mode.md).
- [x] Decision: no outreach to Samsung. Use publicly available material and existing authorized local interfaces only.
- Gate: confirm supported deployment, permissions, uninstall/recovery before any device installation.

## Phase 5 — audio architecture
- [ ] Establish capture format, microphone permission and mute/indicator behavior.
- [x] Identify published MT8532 PCM and FFP processing configuration; runtime availability and permissions remain unverified.
- [ ] Evaluate playback coexistence and explicit activation.
- Gate: no audio recording until consent, mute behavior and indicators are verified.

## Phase 6 — prototype
- [x] Host-side test with synthetic audio and documented Assist protocol (run 45683705531).
- [x] Prepare metadata-only ALSA inventory probe for an authorized native environment; host test run 45716235152.
- [ ] Device prototype only if the supported deployment and capture gates pass.
- [ ] Verify playback, HDMI/eARC, updates and rollback.

## Latest evidence
- Device explicitly reports Tizen 8.0; see [platform and SDK findings](findings/2026-11-25-platform-sdk.md).
- Native API candidates identified; supported soundbar deployment remains the primary gate.

- SmartThings cloud profile confirms OCF NetworkAudio and no registered hub. No supported Edge deployment or microphone capture capability found; see [profile review](findings/2026-11-25-smartthings-profile.md).

- Local OCF confirms smartThingsHub.isSupported=0. InfoLink exposes a disabled HyperUART setting; comparative HW-Q800A research links HyperUART to debugging, but no supported HW-S800D procedure verified. See [OCF comparison](findings/2026-11-25-ocf-comparison.md).

- HyperUART review: older HW-Q800A demonstrates USB network debugging; no verified activation or recovery workflow for 2024 devices. Broaden public research to the shared SAT-MT8532D24WWC firmware family. See [HyperUART review](findings/2026-11-25-hyperuart.md).

- Published Q800D source identifies Linux 5.4.249, ARM32 media binaries, ALSA digital mic capture and a 16 kHz FFP route. Q990D comparison uses different media package. Several aliases and FFP plugin runtime availability are unverified; no native deployment path found. See [source findings](findings/2026-11-25-mt8532-audio-sdk.md).

## Decision paths
A: supported native application (preferred for integration).
B: documented network audio interface (simpler if available).
C: vendor-supported firmware extension only if documented and recoverable.
D: external microphone satellite with soundbar audio output, only as a fallback; does not satisfy native microphone goal.

Excluded by project owner: Alexa Skills and any Alexa-mediated assistant routing. No manufacturer outreach.

## Boundaries
No flashing, modifications to production settings, authentication bypass, private audio collection, or proprietary firmware redistribution. Public research reports contain only sanitized facts. Automated CI limited to tests and explicit firmware-tool changes; no persistent firmware artifacts.

# UltraSlimAssistant — Research and implementation roadmap

Updated: 2026-11-26. This is the canonical working plan; update it after each verified milestone. Historical observations remain in [findings](findings/).

## 1. Objective and scope

Turn the Samsung HW-S800D into a Home Assistant Assist voice satellite using its existing microphones and speakers, independently of Alexa, without additional microphone hardware. Preserve normal HDMI/eARC, TV, music, radio, volume, standby, source switching and physical microphone mute functions. Prefer a lightweight native client on the soundbar and keep STT, conversation/AI and TTS on the Home Assistant server. Wake-word placement is subject to measured resource and audio constraints.

Target: HW-S800D/EN; device-reported firmware SAT-MT8532D24WWC-1072.1. The public USB package is an older reference, not a confirmed exact match.

## 2. Baseline and evidence

- Target OCF /oic/p reports Tizen 8.0, firmware SAT-MT8532D24WWC-1072.1; LAN REST metadata reports developerMode=0 and TCP 26101 was refused in two bounded owner-network checks. These are actual target observations, not proof of TV compatibility. See [platform evidence](findings/2026-11-25-platform-sdk.md) and [service inventory](findings/2026-11-25-service-inventory.md).
- Official S800D USB archive was already inventoried (1,289,225,604 bytes; SHA256 2fcb3c246031a7f5687fb4a1f4a98f8063a63b2ce74e06a900ac5022a8d0a29d). MediaTek MSD metadata includes cryptographic tokens and high entropy; likely opaque/encrypted, not a confirmed exact installed version. See [inventory](findings/2026-11-25-inventory.md) and [MSD inspection](findings/2026-11-25-msd.md).
- Q800D and Q990D published source archives have been inventoried and compared. Kernel, AV SDK, MM_DTV and PulseAudio component hashes match; this does not establish equivalence to the S800D. Some nested archives and files remain unexamined.
- Published Q800D sources show Linux 5.4.249, MT8532 audio drivers, ALSA and PulseAudio 15.0. Selected released audio binaries are 32-bit ARM; the running S800D ABI is not verified.
- Tizen 6.0 tv-samsung native service packaging is present in the released SDK; this is not evidence of third-party installation permission.
- Capture_Mic_normal is a digital microphone route candidate. The configured ffp_in/mtkffp path uses a 16 kHz six-channel input (four mic + two reference channels in comments) and two client channels; negotiated output, plugin presence and active deployment are unverified. Default capture is not necessarily processed. Capture_Voice_Upload is a null PCM; Capture_Echo_Reference is not a speech source.
- HyperUART USB-network code exists in the common source. This does not establish runtime activation, SDB availability or authorized developer access.
- ALSA metadata inventory compiled on a Linux host and passed a synthetic configuration test; the Assist prototype passed nine host tests. Neither establishes target execution or microphone access.
- Repository text write test succeeded (91af6e04); workflow creation permissions are not confirmed.
- No native application has been installed, no soundbar microphone opened, no audio recorded and no device modification made.

Evidence: [MT8532/audio/SDK findings](findings/2026-11-25-mt8532-audio-sdk.md), [source analysis](findings/2026-11-25-source-first-pass.md), [Actions](https://github.com/andreassamitsch/UltraSlimAssistant/actions).

## 3. Target architecture (proposed)

Soundbar microphones -> supported capture interface / existing speech processing -> lightweight UltraSlimAssistant client -> Home Assistant Assist pipeline (STT, conversation, TTS) -> authorized soundbar playback. Local wake word or server-side wake word will be chosen after feasibility and latency tests. Reuse existing echo cancellation and audio focus/ducking only if verified on the target. Preserve physical mute and explicit recording indication.

## 4. Prioritized work packages

### P0 — Native execution and target verification

- [ ] Investigate model-specific documented developer mode, supported native package/service deployment, package manager, TPK signing and authorization, and supported SDB/USB interfaces. Direct source review (work cycle 4) confirms the shared AV SDK spec builds for Tizen 8.0 and uses a vendor-signed firmware preload path; MT8532 audio systemd units are installed by a vendor RPM. Neither establishes owner-accessible deployment. See [native service deployment findings](findings/2026-11-26-native-service-deployment.md). Distinguish TV SDK documentation from actual soundbar support.
- [ ] Determine whether an owner-authorized, vendor-supported way to start a small diagnostic program exists without replacing firmware. Verify a safe stop/uninstall and recovery path before any device-side test. Do not bypass signing, authentication or other access controls.
- [x] Close exact S800D source acquisition as a prerequisite. On 2026-11-26 the owner supplied the complete five-result Samsung TV & Video > AV listing: HW-Q990D.zip, HW-Q800D.zip (Q700D/Q800D/Q930D and AVR equivalents), 17_AV_HawkA_Tizn3.0.zip, 15_WAM7500.zip and BD_E5300.zip. No S800D entry. Owner confirms no further Samsung material is expected. This is owner-reported catalog evidence, not an independently verified exhaustive global search. Do not spend further cycles on the portal or contact Samsung.
- [ ] Use Q800D as primary MT8532 audio reference and Q990D for common platform comparison; verify findings against existing target observations and authorized target diagnostics if new evidence warrants them. Older HawkA Tizen 3.0 is a historical reference only if a concrete question requires it; WAM and Blu-ray packages are low priority. No assumption of exact source or hardware equivalence.

Decision gate: a documented, authorized installation/execution path with rollback and known target prerequisites. If no such path can be established, mark M1 blocked and reassess feasibility rather than treating generic platform features as access.


Work cycle 6: [Service Manager comparison](findings/2026-11-26-service-manager-comparison.md) verifies matching vendor package versions on Q700C/Q935GF and S800D, and the difference between Roon package presence and certified functionality. No owner-installable service API established. Next prioritize supported headless Tizen development profiles and independent service lifecycle testing in a supported SDK/emulator; do not infer target installability.

### P1 — Targeted audio, voice-service and firmware analysis

Work cycle 5: [audio service boundaries](findings/2026-11-26-audio-service-boundaries.md) establishes the reference ALSA configuration chain, separate assistant playback candidate and kernel-level control boundary. No supported deployment or capture interface established on target; physical mute remains unverified. Prioritize model-specific application lifecycle/interface evidence over further generic DSP tracing.

- [x] Inventory the official S800D USB firmware offline and inspect MediaTek MSD metadata/entropy (completed 2026-11-25). Revisit only with new firmware/version or concrete supported format evidence; do not repeat broad scans of the opaque image.
- [ ] Map published/documented Alexa and other existing voice-service architecture: lifecycle, wake word, microphone stream handoff, audio focus/ducking, mute handling and any supported extensibility interface. Do not intercept private assistant traffic, reuse credentials or impersonate an existing provider.
- [ ] Trace FFP and PulseAudio source selection, installed configuration dependencies (including Tizen device-map.json / stream-map.json and vendor audio policy if present), PCM aliases, audio permissions, public recorder API, sample format negotiation and potential processing/echo cancellation. Identify which findings are generic and which are target-specific.
- [ ] Improve reproducibility using the existing source-analysis.yml and tools/source_analysis.py. On 2026-11-26 added focused voice-service, FFP, audio-focus and microphone-privacy matches, local ZIP input and S800D source-name support, with synthetic fixtures (commit b1b9e7b). Existing push workflow self-test passed (run 45738249439, actual job logs verified). Work cycle 2 adds focused voice scope, metadata-only candidate filenames and tested local ZIP CLI (commit a2ddefa, run 45738570453, actual logs verified). Real archive acquisition needs a separately authorized manual run. Record skipped inputs and inspect actual logs before declaring success.

### P2 — Native diagnostics and Assist integration (gated by M1)

- [ ] Prepare a minimal harmless native diagnostic, targeting the verified ABI and supported SDK. Build/test on the host first, without executing extracted vendor programs. Start/stop it on the device only after the execution and recovery gate is met.
- [ ] Enumerate supported audio sources/capabilities and permissions without opening a PCM or modifying mixer controls. Host implementation now includes Tizen Sound Manager input-device metadata (commit 5e32aea; actual CI logs verified in run 45739179673). Real SDK build and execution remain gated by M1. Some ALSA routes set/lock mixer controls on open; prefer supported high-level capture.
- [ ] With explicit owner approval, verify physical mute, recording indication and a brief intentional microphone capture; confirm format, quality and echo behavior. Do not record household audio without consent.
- [ ] Implement the minimal voice client, connection management, Assist pipeline transport, intentional capture, response playback, timeouts, mute state and clean shutdown. Use host fixtures and local integration tests before device rollout.
- [ ] Test wake word, latency, CPU/memory, network loss and reconnection. Choose local or server-side wake word based on measurements.

### P3 — Coexistence and reliable operation

- [ ] Test TV/HDMI/eARC, music/radio, volume, media ducking/restoration, source changes, standby/wake, physical mute, restart and network outages.
- [ ] Document resource budget, diagnostics, supported install/uninstall/update and recovery procedure; require a reversible opt-in rollout. No firmware flashing in the current research phase.
- [ ] Validate daily use and regressions before considering production readiness.

## 5. Milestones and acceptance criteria

| Milestone | Status | Acceptance criterion |
|---|---|---|
| M0 — Reference platform analysis | Substantially complete; exact target source unavailable | Reproducible reference inventory, audio/SDK findings and clearly documented gaps |
| M1 — Hello World on S800D | Next / blocked pending authorized execution path | A minimal owned program starts and stops through a supported method on the actual device; original behavior is unaffected |
| M2 — Audio source enumeration | Pending M1 | Supported microphone/source metadata and privileges verified on target; no unintended mixer changes |
| M3 — Microphone stream | Pending M2 | Explicitly approved capture reaches HA with verified format and mute behavior |
| M4 — Voice dialogue | Pending M3 | Spoken request reaches Assist, appropriate response plays back, normal media behavior is restored |
| M5 — Wake word | Pending M4 | Reliable opt-in activation (e.g. "Hey KI"), acceptable latency, no capture when physically muted |
| M6 — Production readiness | Pending M5 | Normal soundbar functions, reliability, privacy, clean uninstall and recovery verified |

## 6. Working method and decision log

For each investigation: state the question and expected evidence, choose the smallest useful experiment, execute it if authorized and available, inspect the real results/logs, record findings with provenance, update milestone and task status, and identify the next highest-value step. Repeat within the available session; do not claim unperformed work or successful jobs without evidence. Distinguish verified source facts, host tests, target observations and hypotheses. If a blocker requires owner action, describe the exact blocker and what is needed; continue independent offline work where useful. Do not change the soundbar or create a recurring automation as part of this plan.

Immediate next action: use the verified private [source repository migration](findings/2026-11-26-source-repository.md) for targeted reads. The expanded import succeeded; further broad downloads are not a prerequisite. Based on [native service deployment review](findings/2026-11-26-native-service-deployment.md), distinguish firmware provisioning from supported application deployment and seek model-specific evidence before any installation. P0 (supported native execution) remains the priority, parallel with voice-service and FFP analysis using the available Q800D and Q990D references. Review the [first work-cycle findings](findings/2026-11-26-deployment-and-voice.md) [second work-cycle findings](findings/2026-11-26-focused-source-scan.md) and [third work-cycle findings](findings/2026-11-26-sound-manager.md). Reuse an authorized reference archive for the focused scan; do not wait for exact S800D sources. More general source scans are lower priority. M1 is the key feasibility gate, not a promised result.

## 7. Storage, privacy and safety

Keep original archives, firmware and extracted executable/proprietary files outside Git; do not upload them to LFS, releases, Actions caches or artifacts. The owner authorized a separate companion repository for explicitly license-reviewed source text, with a 500 MB budget and deduplicated component manifests; never store vendor source in this development repository. Use a disposable runner or local disk. Save only reviewed small metadata reports and original analysis. Public logs must not include secrets, local network identifiers, device IDs or proprietary payloads. Previously authorized temporary pCloud links remain in public history/logs and should be revoked by their owner when no longer needed. No execution of extracted vendor binaries on analysis hosts. Use authorized interfaces only; preserve physical microphone mute and privacy controls. No production device changes or recording without explicit approval and a safe rollback path.

Official references:
- https://www.samsung.com/at/support/model/HW-S800D/EN/
- https://opensource.samsung.com/
- https://developer.samsung.com/smarttv/develop/getting-started/quick-start-guide.html (TV SDK, not evidence of soundbar support)

Work cycle 7: [headless Tizen SDK validation](findings/2026-11-26-headless-tizen-sdk.md) establishes official generic Tizen 8.0 service API compatibility: independent lifecycle smoke service and capability/inventory probe both passed actual SDK header syntax checks (run 45743111190). Next real build/link and supported emulator lifecycle test; ARM/AArch64 and S800D deployment remain unverified. No device install, recording or settings changes.

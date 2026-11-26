# Work cycle 2 — focused archive inspection and P0 recheck (2026-11-26)

## P0: authorized deployment and exact S800D sources

The public S800D manual directs readers to https://opensource.samsung.com/ (https://device.report/manuals/samsung-soundbar-user-guide-hw-s800d-s81d-s81gd-s70d-s71d). The AV listing is still inaccessible via web retrieval; exact-model/source-filename searches surfaced manuals rather than a source download. The local analysis environment also cannot resolve opensource.samsung.com or eapi.pcloud.com. This does not establish that either service is globally unavailable. No manufacturer outreach, in accordance with the owner's earlier decision.

Official https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html and https://developer.samsung.com/smarttv/develop/tools/additional-tools/vscode/connecting-to-tv-device.html describe TV Developer Mode, while https://developer.samsung.com/smarttv/develop/faq/application-testing.html excludes native TPK files for TV apps. https://developer.samsung.com/smarttv/develop/getting-started/setting-up-sdk/creating-certificates.html describes valid certificate signing. The TV seller-office registration guide (https://developer.samsung.com/tv-seller-office/guides/applications/registering-application.html) additionally describes a separate smartcontroller.microphone privilege that is restricted to pre-consulted apps; this must not be conflated with a generic microphone feature or native recorder privilege. No S800D-specific supported developer or capture path established.

Existing direct LAN evidence and firmware inspection remain adequate until a new authorized interface or source is available. M1 remains blocked. No device-side commands, settings changes, recording, installation or vendor outreach.

## P1: focused source scanning implemented and verified

Commit a2ddefa adds a default voice scope to tools/source_analysis.py, prioritizing top-level audio, AV SDK, voice, micom, SmartThings and service-management archives; --scope all remains available for broad bounded analysis. Excluded root names are logged; omissions do not establish absence. Voice-related member names are listed as metadata even for unexamined binaries. Sensitive-looking member filenames are skipped. The outer listing is explicitly capped, and the entry limit applies before skips.

[Run 45738570453](https://github.com/andreassamitsch/UltraSlimAssistant/actions/runs/45738570453), job 139637676063: actual logs confirm both synthetic tests PASS, including nested archives, local CLI invocation, SHA256, scope selection, filename evidence, invalid ZIP rejection and exclusion of the synthetic sensitive-name fixture. The analyze job was skipped on push as designed. No actual Samsung archive was inspected in this cycle. Local ZIP input has now been exercised end to end using a synthetic file, not just unit-level matching.

[Source analysis instructions](../source-analysis.md) updated with the focused scope, local CLI and direct workflow link. No new workflow was required. The connector does not expose secret creation or manual dispatch. The existing public share links were temporary; their present validity has not been established. A valid authorized archive and manual workflow run are required for new source findings. Do not retain source archives or device dumps in Git.

## Next

1. Obtain a currently authorized public reference or exact S800D archive and run the existing focused analyzer. Inspect actual job logs, then target voice-service, FFP, focus and privacy declarations, rather than repeat broad scans.
2. Keep P0 open until new model-specific evidence establishes a supported native runtime or documented capture interface; do not infer access from generic Tizen SDK capabilities.
3. Reconcile duplicate roadmap documents with the canonical research.md and retain explicit exclusions and evidence levels.

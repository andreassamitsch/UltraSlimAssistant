# Native Tizen capability probe

The HW-S800D reports Tizen 8.0. Generic Tizen documentation describes system_info_get_platform_bool for microphone and media.audio_recording features. The component in prototype/tizen/capability_probe.c queries these two values and now exposes report_input_devices(FILE*) using the documented Sound Manager input/bidirectional device list. It reports device type and direction only, no identifiers or names, and never opens a capture stream, changes volume, routes audio, or changes settings. The new function frees the list on successful retrieval even when enumeration fails, and reports incomplete results separately from an empty list.

References:
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/guides/device/system.md
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/api/overview.md
- https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html
- https://www.samsung.com/at/support/model/HW-S800D/EN/

## Status and gate
The public TV SDK instructions require developer mode on a supported TV; no corresponding soundbar workflow has been verified. A source component is not an installable Tizen app. Host CI compiles against a narrow test stub and checks true/false/error cases; this does not establish real SDK compilation or device support. Do not install on the soundbar until a supported installation mechanism and appropriate SDK profile are established. No manufacturer outreach.

## Local interfaces
The subsequent bounded LAN checks are documented in [service inventory](findings/2026-11-25-service-inventory.md): standard SDB refused, developerMode=0. No supported developer activation established. Published 2024 soundbar IP-control integrations document playback/control, not microphone capture. No active probe, recording, installation or modification performed.

## Next decision
If a supported deployment path is established, compile against the actual target SDK and run capability queries first. A true feature flag alone does not grant recording permission or access to the far-field DSP. Preserve physical microphone mute and status indicators. If no supported path is found, prioritize a separate microphone satellite rather than treating a speculative native component as functional.

## Sound Manager metadata probe (2026-11-26)
Official [Tizen Sound Manager guide](https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/guides/multimedia/sound-manager.md) documents device list retrieval, iteration, type/direction queries and cleanup. Prefer this high-level path to ALSA PCM opening. Generic [Tizen multimedia porting guidance](https://github.com/Samsung/tizen-docs/blob/master/docs/platform/porting/multimedia.md) describes system-mode PulseAudio and board-specific device/stream maps. These are configuration leads, not verified files on HW-S800D. The host stub is deliberately not a vendor ABI. Commit 5e32aea adds synthetic tests for successful enumeration, output exclusion, no devices, permission/error on initial query, partial failure and cleanup failure. CI result must be verified before claiming success. No target SDK compile or installation.

# Native Tizen capability probe

The HW-S800D reports Tizen 8.0. Generic Tizen documentation describes system_info_get_platform_bool for microphone and media.audio_recording features. The component in prototype/tizen/capability_probe.c queries only these two values; no capture, network, settings changes, or device identifiers.

References:
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/guides/device/system.md
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/api/overview.md
- https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html
- https://www.samsung.com/at/support/model/HW-S800D/EN/

## Status and gate
The public TV SDK instructions require developer mode on a supported TV; no corresponding soundbar workflow has been verified. A source component is not an installable Tizen app. Host CI compiles against a narrow test stub and checks true/false/error cases; this does not establish real SDK compilation or device support. Do not install on the soundbar until a supported installation mechanism and appropriate SDK profile are established. No manufacturer outreach.

## Local interfaces
Existing Home Assistant network_scanner device registry lookup returned no devices for that integration; direct LAN service availability remains unmeasured. Published 2024 soundbar IP-control integrations document playback/control, not microphone capture. No active probe, recording, installation or modification performed.

## Next decision
If a supported deployment path is established, compile against the actual target SDK and run capability queries first. A true feature flag alone does not grant recording permission or access to the far-field DSP. Preserve physical microphone mute and status indicators. If no supported path is found, prioritize a separate microphone satellite rather than treating a speculative native component as functional.

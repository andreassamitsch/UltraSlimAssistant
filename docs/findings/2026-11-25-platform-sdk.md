# Platform and SDK research — 2026-11-25

## Verified on HW-S800D
Read-only LocalThings OCF platform resource /oic/p reports mnos=Tizen, mnpv=8.0, mnfv=SAT-MT8532D24WWC-1072.1, mnmo=HW-S800D. /oic/d reports oic.d.networkaudio and icv=core.1.1.0. This confirms device-reported platform version; actual kernel, ABI and SDK subset remain unknown.

## LocalThings review
Reviewed upstream main source:
- https://github.com/mbillow/localthings/blob/main/custom_components/localthings/registry/by_type/soundbar.py
- https://github.com/mbillow/localthings/blob/main/custom_components/localthings/registry/capabilities/soundbar.py (blob 134309e90ed2de1b4aaba3bac55700ec32cd5041): mic is described as static has-a-mic flag; downloadableApp and voice-assistant capabilities do not establish third-party deployment or audio capture.
- https://github.com/mbillow/localthings/blob/main/custom_components/localthings/media_player.py: media playback controls, not microphone transport.
- https://github.com/ZtF/hass-samsung-soundbar-local: documented local playback/control integration, not microphone streaming.

Existing OCF diagnostics confirm authorized control and device identity; no supported PCM capture path was identified. A direct LAN service inventory could not be performed with the available read-only HA interfaces. No active probe or recording attempted.

## Native SDK candidates
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/guides/device/system.md — feature queries for microphone and media.audio_recording.
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/guides/multimedia/raw-audio.md — documented audio input API (audio_in_create, audio_in_prepare, audio_in_read).
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/api/overview.md — common native APIs since 8.0, device capability still must be checked.
- https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html — official developer deployment documented for TVs, not evidence that the S800D supports it.
- https://github.com/Samsung/tizen-docs/blob/master/docs/application/native/reference/security-privileges.md — application signing and declared privileges.
- https://contributors.home-assistant.io/core/internals/assist-pipelines/ — documented Assist WebSocket pipeline for audio input and response; host-side development can be independent of capture hardware.

## Manufacturer
Official source portal https://opensource.samsung.com/ returned HTTP 520 in this research environment. No matching source archive located. Samsung publicly lists oss.request@samsung.com for source requests (https://www.samsung.com/us/support/legal/LGL10000309/). Inquiry draft in repository; not sent.

## Gates
A native probe is appropriate only after a supported installation path is confirmed. First query SDK feature support; then test explicit activation, hardware mute and visible indicators before actual recording. No evidence yet of processed far-field audio or echo cancellation access. Do not equate reported Tizen version with public SDK compatibility. No production device or HA settings modified.

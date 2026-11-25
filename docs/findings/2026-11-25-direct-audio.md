# Direct Assist on HW-S800D — current feasibility

Project owner excludes Alexa Skills and manufacturer outreach. Primary goal remains the original microphone array and soundbar speakers, with direct Home Assistant Assist.

## Evidence
- Device reports Tizen 8.0 and microphone support, but no PCM stream was found in the LocalThings OCF responses.
- Public 2024-series IP-control integration supports HW-S800D on TCP 1516, primarily device control, not microphone capture: https://github.com/ZtF/hass-samsung-soundbar-local
- Samsung documents Developer Mode for TVs, not this soundbar: https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html
- Samsung TV application FAQ says TV applications do not support native .tpk packages: https://developer.samsung.com/smarttv/develop/faq/application-testing.html ; the soundbar SDK/profile is unknown.
- HW-S800D manual describes A2DP playback, not a supported Bluetooth microphone path: https://manualsfile.com/product/k47yn687sus.html
- Tizen upstream explicitly includes audio devices as a product category: https://github.com/Samsung/tizen-docs/blob/master/docs/platform/what-is-tizen/overview.md ; this does not establish third-party app support on HW-S800D.

## Remaining direct path
Check whether the device exposes the documented Tizen SDB developer service on the local network (TCP 26101) and compare with known IP control (TCP 1516). A simple connection test from the owner's trusted LAN can establish TCP reachability only; it cannot establish protocol identity, authorization or application install support. Use a user-supplied local address; no IP stored in repository. No service is assumed available. No port scanning beyond these two documented ports, authentication attempts, configuration changes or installation.

Current connected tools have not provided a LAN terminal or a direct service test; the check remains unperformed. If a documented authorized developer route is available, establish target profile and actual SDK compilation before deploying the capability probe. Otherwise the native path remains unresolved.

## Distinct fallback
External microphone with direct Assist, soundbar for TTS output. Existing projects provide output routing, e.g. https://github.com/jxlarrea/voice-satellite-card-integration and https://github.com/bigbabol1/HomeAssistant_mic_to_mediaplayer . Compatibility, playback interruption and echo cancellation would need validation. This is not a solution using the soundbar microphone. No Alexa Skill, device change or manufacturer contact.

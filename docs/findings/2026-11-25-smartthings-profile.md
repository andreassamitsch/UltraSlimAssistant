# SmartThings cloud profile — 2026-11-25

Owner supplied the SmartThings Advanced device details and Hub list. The latter shows no registered hubs across all locations. Device profile/presentation VD-NetworkAudio-003S; type OCF; execution location Cloud; model HW-S800D; Tizen 8.0; firmware SAT-MT8532D24WWC-1072.1. No sec.smartthingsHub capability shown. The installed hub package previously observed does not establish an active or eligible hub. No Edge installation route verified.

## Capability observations
- execute.execute and ocf.postOcfCommand: device resource operations, not general program execution. Public integrations use execute to access sound mode, EQ and advanced audio OCF resources.
- audioNotification: playTrack, playTrackAndRestore, playTrackAndResume are output functions, not capture. Official reference distinguishes volume restoration from resuming playback. Device implementation untested.
- samsungvd.supportsFeatures.executableServiceList has no reported value; unknown, not proof of an empty supported service list.
- sec.diagnosticsInformation advertises dumpType=file, logType=[errCode,dump], endpoint=PIPER and protocolType=ble_ocf. No associated command in supplied list. Not evidence of an accessible log download, audio capture, or developer access.
- sec.wifiConfiguration describes BLE OCF provisioning, not a development interface.
- No microphone capture, audio stream or app install capability identified in the supplied 23 commands. No commands were sent. Raw JSON not inspected.
- Device/owner/location identifiers, MAC addresses, rules and account data intentionally omitted.

## Sources
- https://developer.smartthings.com/docs/devices/capabilities/capabilities-reference
- https://developer.smartthings.com/docs/devices/capabilities/
- https://github.com/acbee/homeassistant-samsung-soundbar
- https://github.com/home-assistant/core/issues/131362 (same presentation profile, different model)
- https://community.smartthings.com/t/hw-q990b-q995b-the-app-can-control-the-sound-mode-but-i-cannot-find-it-in-smart-things-capabilities/247058

## Decision
Do not create a SmartThings product or attempt Edge deployment without a supported hub. LocalThings already provides authorized access to known OCF resources. Prefer comparison of capability definitions with the existing local resource inventory; only documented/authorized diagnostics, no blind execute commands or private diagnostic dumps. Native deployment and microphone gates remain unresolved. No Alexa or Samsung outreach.

# Local OCF versus SmartThings profile

Read-only refresh of LocalThings diagnostics yielded 68 resources. Compared with owner-supplied SmartThings cloud profile, the local data exposes additional system and audio settings.

| Resource | Observations |
|---|---|
| /sec/networkaudio/smartThingsHub | isSupported=0, state=Default; no hub identity/type. Some generic hubStatus flags are true despite unsupported flag. No Edge deployment route. |
| /sec/networkaudio/infoLink | isSupported=1, infoLinkVersion=T-INFOLINK2024-1000; hyperUARTSetting.currentsetting=OFF; enumerated options HyperUart 1–5 and AT-HUB 1–5. serialLogSetting redacted. |
| /sec/networkaudio/sesInfo | isSupported=1, sesVersion=3.2.276, sesApiLevel=15, updateStatus=UPDATED. Exact subsystem meaning unverified. |
| /sec/networkaudio/av/support | soundApp.isSupported=true; wifiUpdateSupport=true; roonReady reports unavailable. No public install API established. |
| /sec/networkaudio/downloadableApp | Vendor app inventory and update flag only; no documented third-party deployment. |
| /sec/networkaudio/mic | micsupport=1, no capture data or stream. |
| /sec/networkaudio/vasupport | supportedVA=[alexa]; no selectable Assist backend. |
| /sec/networkaudio/bixbysettings | wakeupWord and other Bixby configuration fields noValue; generic far-field flags true, semantics unverified. |
| /devicelog/dump | Timestamp and log ID fields, not actual log content. |
| /devicelog/connectioninfo | devicelog.version=1.0; no log download protocol established. |
| /x.com.samsung/notification/receiver | Audio notification capability, output only. |

## Comparative evidence
Matthew Garrett's 2026-10-30 report on HW-Q800A explicitly connects HyperUART to the Tizen debug service and a USB network adapter. His report also states that newer soundbars lack the legacy listener used on his model: https://codon.org.uk/~mjg59/blog/p/getting-google-cast-on-my-soundbar/ . This is significant comparative evidence but does not demonstrate an authorized, supported developer workflow on HW-S800D. The same article identifies TCP 8443 as Cast API on the older model, suggesting a candidate classification rather than proof of the S800D service role.

## Decision
Prioritize publicly documented HyperUART purpose and supported HW-S800D accessory/service documentation. No write to infoLink, firmware server settings, UART configuration, app-upgrade controls or developer authentication attempted. No raw device logs, account data or private identifiers retained. No Samsung outreach, no Alexa Skills. Original microphone access and supported deployment remain unresolved.

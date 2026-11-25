# SmartThings service menu and application baseline

Owner screenshot shows device pairing, Alexa settings, Spotify Connect and Google Cast. No add-service or app-store control visible in supplied view.

Read-only LocalThings snapshot:
- downloadableApp.isSupported=1, appUpgrade=true
- roon-ready 24.26.10060
- samsung-cloud 3.2.18
- samsung-service-manager 5.0.20
- smartthings-client 4.0.166
- smartthings-hub 6.62.13
- smartthings-thing 5.0.22
- iot-hub-control 2.80.186
- googlesupport: chromecastsupport=1, googletosagreement=1, chromecastversion=2, googleusagereport=0
- vasupport: supportedVA=[alexa], defaultVA=alexa
- av/support: soundApp.isSupported=true; Roon reports unavailable

Google Cast is already supported and its terms accepted, yet no explicit Cast package is present in this particular app inventory. Alexa and Spotify likewise not named there. Inventory may be partial; no evidence the visible menu installs packages or accepts custom services. Ask owner to inspect Google Cast and Spotify screens without changing settings. Avoid disabling Cast because existing HA audio applications use soundbar playback. Compare package inventory and relevant capability values if an actual supported service installation becomes available. No activation, playback, update or configuration change performed.

## UI follow-up
Owner screenshot of Spotify Connect shows instructions and Spotify linking only. Owner reports tapping Google Cast launches Google Home. These observations favor a configuration/account-linking UI for supported services, not a general application installer. They do not prove the implementation is entirely preinstalled or exclude independent package updates. No service activation or disabling required for this comparison. Prioritize published source analysis for package management, service-manager, downloadableApp, audio APIs and supported deployment interfaces. No settings changed.

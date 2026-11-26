# Work cycle 6 — Samsung Service Manager comparison (2026-11-26)

## Evidence
The existing owner-authorized S800D read-only snapshot reports samsung-service-manager 5.0.20, downloadableApp.isSupported=1 and appUpgrade=true, seven reported packages, Alexa as the supported/default VA and no value for executableServiceList. These observations are from the prior target investigation, not a new live query.

Directly inspected public LocalThings fixtures:
- https://github.com/mbillow/localthings/blob/main/tests/fixtures/soundbar_q700c_device.json : six reported packages, Service Manager 5.0.20, SmartThingsHub 6.62.13, smartthings-thing 5.0.22, appUpgrade=true.
- https://github.com/mbillow/localthings/blob/main/tests/fixtures/soundbar_q935gf_device.json : seven packages, same three versions, appUpgrade=true, newer Roon package.
- Both expose downloadableApp as an OCF read/write and baseline resource. The captured representation contains support, appDetail and appUpgrade fields. An interface label does not specify supported write semantics or authorize installing custom packages.
- S61B and Q850A fixtures contain microphone and VA capability resources but no downloadableApp entry in the inspected capture. Q990H fixture did not contain these paths in the inspected structure. Missing fixture data is not proof of missing firmware functionality.
- https://github.com/mbillow/localthings/blob/main/custom_components/localthings/registry/capabilities/soundbar.py (blob 134309e90ed2de1b4aaba3bac55700ec32cd5041), lines 872–901: mic is treated as static capability; downloadableApp and related resources are coverage-only metadata, not an implemented app install command.
- Public app-ID list https://github.com/arlogilbert/tizen-app-id/blob/main/README.md also lists the same Samsung Service Manager and several shared app IDs. This is supplementary cross-platform evidence, not an API specification.
- Complete private snapshot tree listing (9,395 entries, not truncated) had no filenames matching service-manager, downloadableApp, package manager or the two previously proposed audio maps. This is a filename check of a filtered snapshot, not exhaustive content or original archive search.

## Roon as independent cross-check
Official Roon partner list https://roon.app/en/partners/206/samsung lists S800D, Q800D and Q990D as Roon Tested, while later models such as Q800F and Q990H are Roon Ready. Roon documents manufacturer firmware integration and certification at https://help.roonlabs.com/portal/en/kb/articles/roon-ready and https://help.roonlabs.com/portal/en/kb/articles/roon-partner-programs . A roon-ready package in the actual S800D inventory despite unavailable Roon functionality is a concrete example that package presence does not establish a usable service. No generic partner installation API established.

## Interpretation and decision
A shared vendor service lifecycle/updater is the best-supported working hypothesis, not a demonstrated general-purpose user app installer. The exact internal role of Service Manager cannot be established from version metadata. SmartThings capability documentation https://developer.smartthings.com/docs/devices/capabilities/ distinguishes attributes from commands. Official Samsung TV application testing FAQ https://developer.samsung.com/smarttv/develop/faq/application-testing.html and public soundbar update guide https://www.samsung.com/at/support/tv-audio-video/anleitung-zur-aktualisierung-der-soundbar/ do not establish an owner-accessible native soundbar application distribution path.

M1 stays open. Do not send undocumented write requests, alter update server settings, trigger downloads, impersonate manufacturer services or install packages. No target interaction, archive download or private data publication in this cycle. Next useful work: investigate officially supported headless Tizen development/runtime profiles and compare with known target evidence; prepare a minimal independent service lifecycle test in a supported SDK/emulator if available, without representing it as S800D deployment. Avoid repeating generic audio or package-inventory scans without new evidence.

# Work cycle 13 — target diagnostics coverage (2026-11-26)

## Actual read-only inspection
Read the existing S800D LocalThings integration diagnostics via Home Assistant, including the registered integration WebSocket command inventory. The redacted snapshot reports 82 resource-link records (not necessarily 82 unique live endpoints). Upstream LocalThings diagnostics.py, blob 969ed2dbf056a534dc365c3e8b2b52e4e9677e59, describes this as a snapshot of cached/raw device state, not a live process inventory. Freshness metadata was empty in the returned snapshot. No new direct device protocol request was issued.

Relevant resources:
- /capability/sec.diagnosticsInformation/main/0: sensor/baseline metadata, logType errCode and dump, minVersion 3.0, protocolType ble_ocf, dumpType file. Endpoint and setup identifiers not retained.
- /devicelog/connectioninfo and /devicelog/dump: actuator/baseline interfaces with version/connectioninfo and timestamp/logid fields respectively. /devicelog/file is advertised in resource links, but no corresponding representation was identified in the snapshot. No dump content read or requested.
- /sec/networkaudio/sesInfo: support=1, SES version 3.2.276, API level 15, updateStatus UPDATED. SES internal role and package authorization policy not inferred from names.
- /sec/networkaudio/downloadableApp: seven packages and upgrade=true, Service Manager 5.0.20, same known inventory. Not a complete OS package list.
- /sec/networkaudio/infoLink: HyperUART OFF, same ten non-OFF mode choices. Other server settings and device identifiers intentionally not retained.
- /sec/networkaudio/mic: micsupport=1, capability only, not current mute state.
- /sec/networkaudio/vasupport: Alexa is the only listed supported VA.
- No process list, SDB status, developer authorization or native installation command identified. Integration WebSocket command list empty.

## Client limitations
Upstream LocalThings registry/capabilities/soundbar.py blob 134309e90ed2de1b4aaba3bac55700ec32cd5041 lists diagnostic and log resources as coverage-only capability entries (lines 882–900); it does not implement a supported log download or native package-install workflow in these entries. HA tool discovery returned integration/device diagnostics and HA's own logs, not a documented soundbar system-log collection command. Raw snapshot is not the actual device log.

## Decision
Read-only HA diagnostic route exhausted for current purposes. The device advertises manufacturer diagnostics but no supported dump retrieval procedure or developer lifecycle API was established. Do not call actuator interfaces with guessed payloads or export private device logs. No setting changes, audio, firmware modifications, credentials, or raw diagnostic snapshots committed. M1 remains unverified. A further meaningful step needs either a documented owner-accessible diagnostic export with relevant service status or a controlled physical transport experiment with the owner accepting uncertain feasibility; the owner's current software-first purchase condition is not met. No repeated generic source scan recommended.

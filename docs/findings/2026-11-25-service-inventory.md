# LAN service inventory — 2026-11-25

MCP Diagnostics 0.1.3 and 0.1.4 were installed and run on the owner's HA app container. No audio, control commands, credentials, developer authentication or device configuration changes. Source: https://github.com/andreassamitsch/HausCheckHAOS/tree/main/mcp_diagnostics

## Observations
- 22 fixed TCP candidates: 7 open (1516, 8001, 8002, 8008, 8009, 8080, 8443), 15 refused. Standard SDB TCP 26101 refused on both runs. Not a complete port scan.
- mDNS: three target replies; _airplay._tcp.local, _raop._tcp.local, _tidalconnect._tcp.local. No SSDP target reply; container multicast restrictions may affect results.
- HTTP 8001 /api/v2/ and HTTPS 8002 /api/v2/ each HTTP 200 JSON. Sanitized metadata on both: developerMode="0", TokenAuthSupport="true", type="Samsung SmartTV", OS="Tizen". This is an actual response from the soundbar, not confirmation of TV app compatibility. Developer flag reports disabled; no supported mechanism for changing it has been established.
- HTTP 8008 /setup/eureka_info HTTP 200 JSON with build_version, cast_build_revision and version keys, consistent with Cast metadata. TCP 8009 reachable, not directly classified.
- HTTP 8080 root HTTP 403, HTTPS 8443 root HTTP 404. Unknown service role. No access-control bypass attempted.
- Local TLS fingerprint requests were credential-free and did not verify server certificates; not appropriate for authentication.
- No microphone transport identified. No standby/awake controlled comparison performed.

## Interpretation and next gate
The native Tizen route remains a candidate because the Samsung API exposes a developerMode field, but an enabled/authorized developer service and compatible deployment profile remain unverified. Look for published soundbar-specific developer documentation or a supported UI/SDK route; do not assume TV Developer Mode instructions work, and do not bypass authentication. Cast/AirPlay/Tidal evidence concerns playback, not microphone capture. No Alexa Skill, Samsung outreach or physical modification.

Comparison reference: https://github.com/CoderChenDQ/tool-cleanyourtv/blob/main/docs/devices/samsung-tizen.md (TV observations only).

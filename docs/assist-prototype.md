# Assist transport prototype

The first hardware-independent component is prototype/assist_stt.py. It validates 16 kHz mono signed 16-bit PCM or WAV and implements the documented Home Assistant Assist WebSocket audio framing over a caller-provided, already authenticated dedicated connection.

Official reference: https://contributors.home-assistant.io/core/internals/assist-pipelines/

Scope: speech-to-text only. No intent execution, playback, microphone recording, network credentials or live HA connection. Tests use synthetic PCM and a fake WebSocket; these verify client-side behavior, not compatibility with a real server. Run locally: python3 -m unittest discover -s tests -v. Separate CI does not download firmware.

Future work: authenticated transport adapter with explicit opt-in, live STT-only test, streaming/event concurrency and cancellation, TTS output and device capture only after supported soundbar deployment and microphone permissions are confirmed.

## Deployment research
Samsung's official TV SDK installation and device connection guides require Developer Mode on supported TVs. No equivalent documented HW-S800D developer workflow was found. Generic Tizen 8 API availability does not establish support on this soundbar.
- https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html
- https://developer.samsung.com/smarttv/develop/getting-started/setting-up-sdk/installing-tv-sdk.html

Manufacturer source/SDK inquiry remains drafted, not sent. Do not try TV installation instructions on a production soundbar without documented compatibility.

# Assist transport prototype

The first hardware-independent component is prototype/assist_stt.py. It validates 16 kHz mono signed 16-bit PCM or WAV and implements the documented Home Assistant Assist WebSocket audio framing over a caller-provided, already authenticated dedicated connection.

Official reference: https://contributors.home-assistant.io/core/internals/assist-pipelines/

Scope: speech-to-text only. No intent execution, playback, microphone recording, network credentials or live HA connection. Tests use synthetic PCM and a fake WebSocket; these verify client-side behavior, not compatibility with a real server. Run locally: python3 -m unittest discover -s tests -v. Separate CI does not download firmware.

Future work: live STT-only test, streaming/event concurrency and cancellation, TTS output and device capture only after supported soundbar deployment and microphone permissions are confirmed.

## Deployment research
Samsung's official TV SDK installation and device connection guides require Developer Mode on supported TVs. No equivalent documented HW-S800D developer workflow was found. Generic Tizen 8 API availability does not establish support on this soundbar.
- https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html
- https://developer.samsung.com/smarttv/develop/getting-started/setting-up-sdk/installing-tv-sdk.html

Manufacturer outreach cancelled by project owner. No contact. Do not try TV installation instructions on a production soundbar without documented compatibility.

## Live test (explicit opt-in)
Install requirements.txt in a local virtual environment. Run `python -m prototype.live_stt --url wss://YOUR-HA/api/websocket --pipeline PIPELINE_ID --wav test.wav --allow-upload`. Use a valid TLS endpoint, a short synthetic or explicitly approved 16 kHz mono WAV, and a locally entered access token. No token is stored. The selected speech provider may process the uploaded file in the cloud. This test ends at STT; no intents, playback or microphone access. Never put real endpoints, pipeline IDs, audio or credentials in the public repo or CI. The CLI has been implemented but a live connection has not yet been tested.

"""Opt-in STT-only connection test using an explicitly provided WAV file."""
import argparse
import asyncio
import getpass
import json
from urllib.parse import urlsplit
from prototype.assist_stt import read_wav, transcribe

def validate_url(url):
    parts = urlsplit(url)
    if (parts.scheme != "wss" or not parts.hostname or parts.username or parts.password
            or parts.query or parts.fragment or parts.path != "/api/websocket"):
        raise ValueError("Provide a wss:// endpoint ending in /api/websocket")
    return url

async def authenticate(socket, token):
    if not token:
        raise ValueError("Empty token")
    hello = json.loads(await asyncio.wait_for(socket.recv(), 10))
    if hello.get("type") != "auth_required":
        raise RuntimeError("Unexpected authentication greeting")
    await socket.send(json.dumps({"type": "auth", "access_token": token}))
    reply = json.loads(await asyncio.wait_for(socket.recv(), 10))
    if reply.get("type") != "auth_ok":
        raise RuntimeError("Authentication failed")

async def connect(url, token, pcm, pipeline):
    from websockets.asyncio.client import connect as websocket_connect
    async with websocket_connect(validate_url(url), open_timeout=10,
                                 close_timeout=3, max_size=1024*1024,
                                 proxy=None) as socket:
        await authenticate(socket, token)
        return await transcribe(socket, pcm, pipeline)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--wav", required=True)
    parser.add_argument("--pipeline", required=True, help="Explicit STT-capable pipeline ID")
    parser.add_argument("--allow-upload", action="store_true",
                        help="Allow the selected STT provider to receive this audio")
    args = parser.parse_args()
    if not args.allow_upload:
        parser.error("Audio transmission requires --allow-upload")
    try:
        url = validate_url(args.url)
        pcm = read_wav(args.wav)
        token = getpass.getpass("Home Assistant access token (not stored): ")
        result = asyncio.run(connect(url, token, pcm, args.pipeline))
        print(result)
    except Exception as exc:
        # Never dump request objects, tokens, URLs or exception payloads.
        parser.exit(1, f"STT probe failed: {type(exc).__name__}\n")

if __name__ == "__main__":
    main()

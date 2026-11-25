"""Transport-neutral Assist speech-to-text probe. No microphone or playback access."""
import asyncio
import json
import wave

MAX_SECONDS = 15
RATE = 16000
FRAME = 640  # 20 ms, signed 16-bit mono PCM

def read_wav(path):
    with wave.open(str(path), "rb") as wav:
        if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getcomptype()) != (1, 2, RATE, "NONE"):
            raise ValueError("Expected uncompressed mono 16-bit 16 kHz WAV")
        if not 0 < wav.getnframes() <= RATE * MAX_SECONDS:
            raise ValueError("WAV length must be between zero and 15 seconds")
        pcm = wav.readframes(wav.getnframes())
        if len(pcm) != 2 * wav.getnframes():
            raise ValueError("Truncated WAV")
        return pcm

async def transcribe(socket, pcm, pipeline=None):
    """Use an already authenticated, dedicated WebSocket. STT only, no intents."""
    if not isinstance(pcm, bytes) or not pcm or len(pcm) % 2 or len(pcm) > RATE * MAX_SECONDS * 2:
        raise ValueError("Invalid PCM")
    command = {"id": 1, "type": "assist_pipeline/run", "start_stage": "stt",
               "end_stage": "stt", "input": {"sample_rate": RATE}, "timeout": 30}
    if pipeline:
        command["pipeline"] = pipeline
    async def run():
        await socket.send(json.dumps(command))
        handler = None
        transcript = None
        while True:
            msg = json.loads(await socket.recv())
            if msg.get("id") != 1:
                continue
            if msg.get("type") == "result" and not msg.get("success"):
                raise RuntimeError("Assist request rejected")
            if msg.get("type") != "event":
                continue
            event = msg["event"]
            kind = event["type"]
            data = event.get("data") or {}
            if kind == "run-start":
                if handler is not None:
                    raise RuntimeError("Duplicate run-start")
                handler = data.get("runner_data", {}).get("stt_binary_handler_id")
                if type(handler) is not int or not 0 <= handler <= 255:
                    raise RuntimeError("Missing or invalid binary handler")
                prefix = bytes([handler])
                for i in range(0, len(pcm), FRAME):
                    await socket.send(prefix + pcm[i:i+FRAME])
                await socket.send(prefix)
            elif kind == "error":
                raise RuntimeError("Assist pipeline failed")
            elif kind == "stt-end":
                transcript = data.get("stt_output", {}).get("text")
            elif kind == "run-end":
                if not isinstance(transcript, str):
                    raise RuntimeError("No completed transcription")
                return transcript
    return await asyncio.wait_for(run(), timeout=40)

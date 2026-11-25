import json
import unittest
from prototype.assist_stt import transcribe

def event(kind, data=None, id=1):
    return json.dumps({"id": id, "type": "event", "event": {"type": kind, "data": data or {}}})

class FakeSocket:
    def __init__(self, messages):
        self.messages = iter(messages)
        self.sent = []
    async def send(self, value):
        self.sent.append(value)
    async def recv(self):
        return next(self.messages)

class TestAssist(unittest.IsolatedAsyncioTestCase):
    async def test_transcribe(self):
        sock = FakeSocket([
            json.dumps({"id": 1, "type": "result", "success": True}),
            event("run-start", {"runner_data": {"stt_binary_handler_id": 7}}),
            event("stt-start"),
            event("stt-end", {"stt_output": {"text": "Test"}}),
            event("run-end"),
        ])
        pcm = bytes(642)
        self.assertEqual(await transcribe(sock, pcm), "Test")
        command = json.loads(sock.sent[0])
        self.assertEqual(command["end_stage"], "stt")
        self.assertEqual(command["input"], {"sample_rate": 16000})
        self.assertEqual(sock.sent[1:], [b"\x07" + pcm[:640], b"\x07" + pcm[640:], b"\x07"])

    async def test_error(self):
        sock = FakeSocket([event("error", {"code": "stt-provider-missing"})])
        with self.assertRaises(RuntimeError):
            await transcribe(sock, b"\0\0")

    async def test_bad_audio(self):
        sock = FakeSocket([])
        with self.assertRaises(ValueError):
            await transcribe(sock, b"\0")
        self.assertEqual(sock.sent, [])

    async def test_invalid_handler(self):
        sock = FakeSocket([event("run-start", {"runner_data": {"stt_binary_handler_id": 256}})])
        with self.assertRaises(RuntimeError):
            await transcribe(sock, b"\0\0")
        self.assertEqual(len(sock.sent), 1)

    async def test_missing_transcript(self):
        sock = FakeSocket([event("run-end")])
        with self.assertRaises(RuntimeError):
            await transcribe(sock, b"\0\0")

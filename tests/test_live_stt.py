import json
import unittest
from prototype.live_stt import authenticate, validate_url

class FakeSocket:
    def __init__(self, replies):
        self.replies = iter(replies)
        self.sent = []
    async def recv(self):
        return json.dumps(next(self.replies))
    async def send(self, value):
        self.sent.append(json.loads(value))

class TestLiveStt(unittest.IsolatedAsyncioTestCase):
    def test_tls_only(self):
        url = "wss://example.test/api/websocket"
        self.assertEqual(validate_url(url), url)
        for bad in ["ws://example.test/api/websocket", "wss://u:p@example.test/api/websocket",
                    "wss://example.test/api/websocket?token=abc", "wss://example.test/other"]:
            with self.assertRaises(ValueError):
                validate_url(bad)

    async def test_auth(self):
        sock = FakeSocket([{"type": "auth_required"}, {"type": "auth_ok"}])
        await authenticate(sock, "dummy-token")
        self.assertEqual(sock.sent, [{"type": "auth", "access_token": "dummy-token"}])

    async def test_reject(self):
        sock = FakeSocket([{"type": "auth_required"}, {"type": "auth_invalid"}])
        with self.assertRaises(RuntimeError):
            await authenticate(sock, "dummy-token")

    async def test_unexpected_greeting(self):
        sock = FakeSocket([{"type": "result"}])
        with self.assertRaises(RuntimeError):
            await authenticate(sock, "dummy-token")
        self.assertEqual(sock.sent, [])

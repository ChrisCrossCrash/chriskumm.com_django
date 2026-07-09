import json

from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .views import _TOKENS

User = get_user_model()


async def _acollect(chunks):
    return b"".join([chunk async for chunk in chunks])


def _read_streaming(response):
    """The sse view streams an async generator, so its streaming_content is
    async-iterable; ping/download stream plain iterables. Handle both."""
    content = response.streaming_content
    if hasattr(content, "__aiter__"):
        return async_to_sync(_acollect)(content)
    return b"".join(content)


def _parse_sse(body):
    """Parse an SSE byte stream into a list of (id_or_None, data) tuples."""
    events = []
    for block in body.decode().split("\n\n"):
        if not block.strip() or block.startswith("retry:"):
            continue
        event_id = None
        data = None
        for line in block.splitlines():
            if line.startswith("id: "):
                event_id = int(line[len("id: ") :])
            elif line.startswith("data: "):
                data = json.loads(line[len("data: ") :])
        events.append((event_id, data))
    return events


class PingTests(APITestCase):
    def setUp(self):
        self.url = reverse("benchmark-ping")
        self.user = User.objects.create_user(email="test@example.com")

    def test_unauthenticated_returns_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ping_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ping_body(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data, {"ok": True})


class DownloadTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com")

    def _url(self, num_bytes):
        return reverse("benchmark-download", kwargs={"num_bytes": num_bytes})

    def test_unauthenticated_returns_401(self):
        response = self.client.get(self._url(1024))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_zero_bytes(self):
        """Returns 200 with Content-Length 0 and an empty body."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url(0))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Length"], "0")
        self.assertEqual(b"".join(response.streaming_content), b"")

    def test_exact_byte_count(self):
        """Returns exactly the requested number of bytes."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url(1024))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Length"], "1024")
        self.assertEqual(len(b"".join(response.streaming_content)), 1024)

    def test_larger_size(self):
        """Handles a 1 MB download correctly."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url(1048576))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Length"], "1048576")
        self.assertEqual(len(b"".join(response.streaming_content)), 1048576)

    def test_negative_bytes_rejected(self):
        """Django's int URL converter rejects negative values, so the URL doesn't match."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/benchmark/download/-1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_over_cap_rejected(self):
        """Requests over the 100 MB cap return 400."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self._url(100 * 1024 * 1024 + 1))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(DEBUG=False)
class SseTests(APITestCase):
    """Auth uses a real Authorization header rather than force_authenticate
    to exercise the same header path SSE clients use. DEBUG is forced off so
    the auth check always runs."""

    def setUp(self):
        self.url = reverse("benchmark-sse")
        self.user = User.objects.create_user(email="test@example.com")
        self.token = Token.objects.create(user=self.user)
        self.auth_header = f"Token {self.token.key}"

    def test_unauthenticated_returns_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_invalid_token_returns_401(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION="Token bogus")
        self.assertEqual(response.status_code, 401)

    def test_post_returns_405(self):
        response = self.client.post(self.url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 405)

    def test_authenticated_stream_starts(self):
        response = self.client.get(
            f"{self.url}?count=1&interval_ms=0",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/event-stream")
        body = _read_streaming(response)
        self.assertTrue(body.startswith(b"retry: 3000\n\n"))

    def test_event_stream_accept_header_negotiates(self):
        """Regression: EventSource sends `Accept: text/event-stream`, which
        DRF content negotiation rejected with 406 before EventStreamRenderer
        was registered on the view."""
        response = self.client.get(
            f"{self.url}?count=1&interval_ms=0",
            HTTP_AUTHORIZATION=self.auth_header,
            HTTP_ACCEPT="text/event-stream",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/event-stream")
        self.assertEqual(len(_parse_sse(_read_streaming(response))), 1)

    def test_error_with_event_stream_accept_returns_json_body(self):
        """Error responses negotiated to EventStreamRenderer must still
        render a valid JSON body rather than crashing."""
        response = self.client.get(
            f"{self.url}?count=nope",
            HTTP_AUTHORIZATION=self.auth_header,
            HTTP_ACCEPT="text/event-stream",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"count": "must be an integer"})

    def test_count_limits_number_of_events(self):
        response = self.client.get(
            f"{self.url}?count=5&interval_ms=0",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        body = _read_streaming(response)
        self.assertEqual(len(_parse_sse(body)), 5)

    def test_zero_count_sends_no_events(self):
        response = self.client.get(
            f"{self.url}?count=0&interval_ms=0",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        body = _read_streaming(response)
        self.assertEqual(_parse_sse(body), [])

    def test_default_id_every_sends_id_on_every_event(self):
        response = self.client.get(
            f"{self.url}?count=3&interval_ms=0",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        body = _read_streaming(response)
        events = _parse_sse(body)
        self.assertEqual([e[0] for e in events], [0, 1, 2])
        self.assertEqual([e[1] for e in events], _TOKENS[0:3])

    def test_id_every_zero_omits_ids(self):
        response = self.client.get(
            f"{self.url}?count=3&id_every=0&interval_ms=0",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        body = _read_streaming(response)
        events = _parse_sse(body)
        self.assertEqual([e[0] for e in events], [None, None, None])

    def test_id_every_n_sends_id_periodically(self):
        response = self.client.get(
            f"{self.url}?count=6&id_every=3&interval_ms=0",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        body = _read_streaming(response)
        events = _parse_sse(body)
        self.assertEqual([e[0] for e in events], [0, None, None, 3, None, None])

    def test_last_event_id_resumes_after_given_id(self):
        response = self.client.get(
            f"{self.url}?count=2&interval_ms=0",
            HTTP_LAST_EVENT_ID="5",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        body = _read_streaming(response)
        events = _parse_sse(body)
        self.assertEqual([e[0] for e in events], [6, 7])

    def test_invalid_last_event_id_starts_from_zero(self):
        response = self.client.get(
            f"{self.url}?count=1&interval_ms=0",
            HTTP_LAST_EVENT_ID="not-a-number",
            HTTP_AUTHORIZATION=self.auth_header,
        )
        body = _read_streaming(response)
        events = _parse_sse(body)
        self.assertEqual(events[0][0], 0)

    def test_invalid_id_every_returns_400(self):
        response = self.client.get(
            f"{self.url}?id_every=nope", HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, 400)

    def test_negative_id_every_returns_400(self):
        response = self.client.get(
            f"{self.url}?id_every=-1", HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_interval_ms_returns_400(self):
        response = self.client.get(
            f"{self.url}?interval_ms=nope", HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, 400)

    def test_negative_interval_ms_returns_400(self):
        response = self.client.get(
            f"{self.url}?interval_ms=-1", HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_count_returns_400(self):
        response = self.client.get(
            f"{self.url}?count=nope", HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, 400)

    def test_negative_count_returns_400(self):
        response = self.client.get(
            f"{self.url}?count=-1", HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, 400)


@override_settings(DEBUG=True)
class SseDebugModeTests(APITestCase):
    """DEBUG=True bypasses auth entirely. Django forces DEBUG=False for the
    test client regardless of the real settings, so this must be set
    explicitly to exercise that branch."""

    def test_no_token_required_in_debug_mode(self):
        response = self.client.get(f"{reverse('benchmark-sse')}?count=0&interval_ms=0")
        self.assertEqual(response.status_code, 200)

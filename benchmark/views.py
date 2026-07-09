import asyncio
import itertools
import json
from pathlib import Path

from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    renderer_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .permissions import IsAuthenticatedUnlessDebug
from .renderers import EventStreamRenderer

_DOWNLOAD_MAX = 100 * 1024 * 1024
_CHUNK = 65536
_SSE_RETRY_MS = 3000


_auth = [TokenAuthentication]
_perms = [IsAuthenticatedUnlessDebug]

_TOKENS_PATH = Path(__file__).resolve().parent / "tokens.jsonl"
_TOKENS = [json.loads(line) for line in _TOKENS_PATH.read_text().splitlines()]


@api_view(["GET"])
@authentication_classes(_auth)
@permission_classes(_perms)
def ping(request):
    return Response({"ok": True})


@api_view(["GET"])
@authentication_classes(_auth)
@permission_classes(_perms)
def download(request, num_bytes):
    if num_bytes > _DOWNLOAD_MAX:
        return HttpResponse(status=400)

    def _stream():
        remaining = num_bytes
        buf = b"\x00" * _CHUNK
        while remaining >= _CHUNK:
            yield buf
            remaining -= _CHUNK
        if remaining:
            yield b"\x00" * remaining

    response = StreamingHttpResponse(_stream(), content_type="application/octet-stream")
    response["Content-Length"] = num_bytes
    return response


def _int_param(request, name, default=None):
    """Parse a non-negative integer query param, or return `default` if absent."""
    raw = request.query_params.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ValidationError({name: "must be an integer"})
    if value < 0:
        raise ValidationError({name: "must be non-negative"})
    return value


@api_view(["GET"])
@renderer_classes([EventStreamRenderer, JSONRenderer])
@authentication_classes(_auth)
@permission_classes(_perms)
def sse(request):
    # ?id_every=N controls how often an `id` field is sent: 0 = never, 1
    # (default) = every event, N = every Nth event. Lets clients be tested
    # against feeds where the last-seen id isn't the immediately preceding
    # event, which the spec permits.
    id_every = _int_param(request, "id_every", 1)

    # ?interval_ms=N sets the delay between events (default 100).
    interval_ms = _int_param(request, "interval_ms", 100)

    # ?count=N ends the stream after N events for this connection instead of
    # running forever. Unset/absent means infinite.
    count = _int_param(request, "count")

    # Resume just after the last id the client saw, if any. Ids are indices
    # into _TOKENS (mod len), so this works even though the stream cycles
    # forever and content repeats.
    last_event_id = request.headers.get("Last-Event-ID", "").strip()
    try:
        start = (int(last_event_id) + 1) % len(_TOKENS)
    except ValueError:
        start = 0

    # The view itself is sync (DRF handles auth/validation in the worker
    # thread and returns immediately), but the body is an async generator:
    # under ASGI, Django iterates it on the event loop, so the sleeps don't
    # occupy a thread. A sync generator here would pin Django's single
    # thread_sensitive worker thread and block every other sync view for the
    # stream's lifetime.
    async def _stream():
        yield f"retry: {_SSE_RETRY_MS}\n\n".encode()
        sent = 0
        for i in itertools.count(start):
            if count is not None and sent >= count:
                return
            idx = i % len(_TOKENS)
            id_line = f"id: {idx}\n" if id_every and idx % id_every == 0 else ""
            yield f"{id_line}data: {json.dumps(_TOKENS[idx])}\n\n".encode()
            sent += 1
            await asyncio.sleep(interval_ms / 1000)

    response = StreamingHttpResponse(_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response

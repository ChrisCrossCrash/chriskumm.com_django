from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

_DOWNLOAD_MAX = 100 * 1024 * 1024
_CHUNK = 65536

_auth = [TokenAuthentication]
_perms = [IsAuthenticated]


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

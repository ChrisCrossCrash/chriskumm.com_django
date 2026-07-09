import json

from rest_framework.renderers import BaseRenderer


class EventStreamRenderer(BaseRenderer):
    """Lets content negotiation accept `Accept: text/event-stream` (which
    EventSource always sends). The success path returns a raw
    StreamingHttpResponse, so render() only runs for error responses
    (auth failures, ValidationError) — emit those as JSON."""

    media_type = "text/event-stream"
    format = "sse"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps(data).encode()

from rest_framework.permissions import IsAuthenticated
from django.conf import settings


class IsAuthenticatedUnlessDebug(IsAuthenticated):
    """Skip auth in DEBUG so local benchmarking doesn't need a token.
    Checked per-request rather than at import time so override_settings
    works in tests."""

    def has_permission(self, request, view):
        return settings.DEBUG or super().has_permission(request, view)

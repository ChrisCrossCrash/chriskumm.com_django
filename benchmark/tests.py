from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


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

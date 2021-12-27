from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class ArtAPIStatusTestCase(APITestCase):
    fixtures = ["art_standard.json"]

    def test_home_url_returns_200(self):
        response = self.client.get(reverse("art:home"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_pieces_url_returns_200(self):
        response = self.client.get(reverse("art:all_pieces"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_artist_url_returns_200(self):
        response = self.client.get(reverse("art:artist", args=["1"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_artist_list_url_returns_200(self):
        response = self.client.get(reverse("art:artist_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_url_returns_200(self):
        response = self.client.get(reverse("art:location", args=["1"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_list_url_returns_200(self):
        response = self.client.get(reverse("art:location_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_style_url_returns_200(self):
        response = self.client.get(reverse("art:style", args=["1"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_style_list_url_returns_200(self):
        response = self.client.get(reverse("art:style_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

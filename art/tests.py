from pprint import pprint

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Piece, Style, Artist, Location


class ArtAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        artist = Artist.objects.create(name="Bob Ross")
        location = Location.objects.create(
            name="MOMA", city="New York, NY", country="USA"
        )
        style = Style.objects.create(name="Naturalism")
        piece = Piece.objects.create(
            title="Happy Trees",
            artist=artist,
            location=location,
            # TODO: Fix this test by including an image with the test piece.
        )
        piece.styles.add(style)

    def test_home_url_returns_200(self):
        response = self.client.get(reverse("art:home"))
        pprint(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_artist_url_returns_200(self):
        response = self.client.get(reverse("art:artist", args=["1"]))
        pprint(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_url_returns_200(self):
        response = self.client.get(reverse("art:location", args=["1"]))
        pprint(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_style_url_returns_200(self):
        response = self.client.get(reverse("art:style", args=["1"]))
        pprint(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

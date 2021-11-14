from django.http import HttpResponsePermanentRedirect

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from decouple import config

from .models import Piece, Artist, Location, Style
from .serializers import (
    PieceSerializer,
    PieceSerializerWithoutThumbnail,
    ArtistSerializer,
    LocationSerializer,
    StyleSerializer,
)


class ArtPaginationClass(PageNumberPagination):
    page_size = 4


class PieceList(ListAPIView):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    pagination_class = ArtPaginationClass


class AllPieceList(ListAPIView):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializerWithoutThumbnail


class ArtistList(ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class LocationList(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class StyleList(ListAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer


class PiecesByArtistList(ListAPIView):
    serializer_class = PieceSerializer
    pagination_class = ArtPaginationClass

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Piece.objects.filter(artist=pk)


class PiecesByLocationList(ListAPIView):
    serializer_class = PieceSerializer
    pagination_class = ArtPaginationClass

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Piece.objects.filter(location=pk)


class PiecesByStyleList(ListAPIView):
    serializer_class = PieceSerializer
    pagination_class = ArtPaginationClass

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Piece.objects.filter(styles=pk)


def redirect_to_art_front_end(request):
    return HttpResponsePermanentRedirect(config("ART_URL"))

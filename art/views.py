from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from .models import Piece, Artist, Location, Style
from .serializers import (
    InstaArtSerializer,
    ArtistSerializer,
    LocationSerializer,
    StyleSerializer,
)


class ArtPaginationClass(PageNumberPagination):
    page_size = 4


class PieceList(ListAPIView):
    queryset = Piece.objects.all()
    serializer_class = InstaArtSerializer
    pagination_class = ArtPaginationClass


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
    serializer_class = InstaArtSerializer
    pagination_class = ArtPaginationClass

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Piece.objects.filter(artist=pk)


class PiecesByLocationList(ListAPIView):
    serializer_class = InstaArtSerializer
    pagination_class = ArtPaginationClass

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Piece.objects.filter(location=pk)


class PiecesByStyleList(ListAPIView):
    serializer_class = InstaArtSerializer
    pagination_class = ArtPaginationClass

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Piece.objects.filter(styles=pk)

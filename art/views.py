from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from .models import Piece
from .serializers import InstaArtSerializer


class ArtPaginationClass(PageNumberPagination):
    page_size = 2


class PieceList(ListAPIView):
    queryset = Piece.objects.all()
    serializer_class = InstaArtSerializer
    pagination_class = ArtPaginationClass


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

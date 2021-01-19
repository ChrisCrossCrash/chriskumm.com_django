from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Piece
from .serializers import InstaArtSerializer


class InstaArt(APIView):
    # noinspection PyUnusedLocal
    @staticmethod
    def get(request, format=None):
        pieces = Piece.objects.all()
        serializer = InstaArtSerializer(pieces, many=True)
        return Response(serializer.data)


class ArtistView(APIView):
    # noinspection PyUnusedLocal
    @staticmethod
    def get(request, pk, format=None):
        pieces = get_list_or_404(Piece, artist=pk)
        serializer = InstaArtSerializer(pieces, many=True)
        return Response(serializer.data)


class LocationView(APIView):
    # noinspection PyUnusedLocal
    @staticmethod
    def get(request, pk, format=None):
        pieces = get_list_or_404(Piece, location=pk)
        serializer = InstaArtSerializer(pieces, many=True)
        return Response(serializer.data)


class StyleView(APIView):
    # noinspection PyUnusedLocal
    @staticmethod
    def get(request, pk, format=None):
        pieces = get_list_or_404(Piece, styles=pk)
        serializer = InstaArtSerializer(pieces, many=True)
        return Response(serializer.data)

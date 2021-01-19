from .models import Artist, Location, Style, Piece

from rest_framework import serializers


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name', 'pk']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'pk']


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ['name', 'pk']


class InstaArtSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    location = LocationSerializer()
    styles = StyleSerializer(many=True)

    @staticmethod
    def get_image_info(obj):
        return {
            'url': obj.image.url,
            'height': obj.image.height,
            'width': obj.image.width,
        }

    image = serializers.SerializerMethodField('get_image_info')

    class Meta:
        model = Piece
        fields = [
            'title',
            'artist',
            'location',
            'styles',
            'description',
            'wiki_url',
            'image',
        ]

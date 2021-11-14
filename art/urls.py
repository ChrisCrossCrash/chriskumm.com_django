from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "art"

urlpatterns = [
    path("", views.PieceList.as_view(), name="home"),
    path("all-pieces/", views.AllPieceList.as_view(), name="all-pieces"),
    path("artist/<int:pk>/", views.PiecesByArtistList.as_view(), name="artist"),
    path("artist/", views.ArtistList.as_view(), name="artist_list"),
    path("location/<int:pk>/", views.PiecesByLocationList.as_view(), name="location"),
    path("location/", views.LocationList.as_view(), name="location_list"),
    path("style/<int:pk>/", views.PiecesByStyleList.as_view(), name="style"),
    path("style/", views.StyleList.as_view(), name="style_list"),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json", "html"])

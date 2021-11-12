from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "art"

urlpatterns = [
    path("", views.PieceList.as_view(), name="home"),
    path("artist/<int:pk>/", views.PiecesByArtistList.as_view(), name="artist"),
    path("location/<int:pk>/", views.PiecesByLocationList.as_view(), name="location"),
    path("style/<int:pk>/", views.PiecesByStyleList.as_view(), name="style"),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json", "html"])

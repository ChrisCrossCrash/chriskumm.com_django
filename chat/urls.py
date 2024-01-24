from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("echo/", views.echo_room, name="echo_room"),
    path("<str:room_name>/", views.room, name="room"),
]

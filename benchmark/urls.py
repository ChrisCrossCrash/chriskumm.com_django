from django.urls import path
from . import views

urlpatterns = [
    path("ping/", views.ping, name="benchmark-ping"),
    path("download/<int:num_bytes>/", views.download, name="benchmark-download"),
    path("sse/", views.sse, name="benchmark-sse"),
]

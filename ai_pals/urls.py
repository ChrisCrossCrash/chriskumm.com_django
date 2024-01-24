from django.urls import path
from .views import new_character

urlpatterns = [
    path("", new_character, name="ai_pals"),
]

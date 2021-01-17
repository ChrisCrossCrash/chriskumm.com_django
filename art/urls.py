from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'art'

urlpatterns = [
    path('', views.InstaArt.as_view()),
    path('artist/<int:pk>/', views.ArtistView.as_view()),
    path('location/<int:pk>/', views.LocationView.as_view()),
    path('style/<int:pk>/', views.StyleView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

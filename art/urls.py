from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'art'

urlpatterns = [
    path('', views.InstaArt.as_view(), name='home'),
    path('artist/<int:pk>/', views.ArtistView.as_view(), name='artist'),
    path('location/<int:pk>/', views.LocationView.as_view(), name='location'),
    path('style/<int:pk>/', views.StyleView.as_view(), name='style'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

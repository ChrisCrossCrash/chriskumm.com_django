from core.admin import core_admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from art.views import redirect_to_art_front_end

urlpatterns = [
    path("admin/", core_admin_site.urls),
    path("api/art/", include("art.urls")),
    path("art/", redirect_to_art_front_end),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

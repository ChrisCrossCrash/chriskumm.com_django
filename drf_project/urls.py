from core.admin import core_admin_site
from core.views import submit_inquiry
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", core_admin_site.urls),
    path("api/submit-inquiry/", submit_inquiry),
    path("api/art/", include("art.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

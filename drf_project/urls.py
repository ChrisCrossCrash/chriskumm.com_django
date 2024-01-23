from core.admin import core_admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", core_admin_site.urls),
    path("api/art/", include("art.urls")),
    path("api/ai-chat/", include("ai_chat.urls")),
    path("api/ai-pals/", include("ai_pals.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

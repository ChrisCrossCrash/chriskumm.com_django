from django.contrib import admin
from core.admin import core_admin_site

from .models import Artist, Location, Style, Piece


@admin.register(Piece, site=core_admin_site)
class PieceAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "location", "created_date")
    list_filter = ("artist", "styles", "location")
    search_fields = ("title", "artist__name", "style__name", "location__name")
    exclude = ("image_b64_thumbnail",)


core_admin_site.register(Artist)
core_admin_site.register(Location)
core_admin_site.register(Style)

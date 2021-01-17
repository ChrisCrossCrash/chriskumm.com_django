from core.admin import core_admin_site

from .models import Artist, Location, Style, Piece

core_admin_site.register(Artist)
core_admin_site.register(Location)
core_admin_site.register(Style)
core_admin_site.register(Piece)

from solo.admin import SingletonModelAdmin
from core.admin import core_admin_site
from .models import SystemMessage


core_admin_site.register(SystemMessage, SingletonModelAdmin)

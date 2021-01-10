import logging
from django.conf import settings

CUSTOM_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_not_maintenance_mode_503': {
            '()': 'drf_project.custom_logging.RequireNotMaintenanceMode503',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': [
                'require_debug_false',
                'require_not_maintenance_mode_503',
            ],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


class RequireNotMaintenanceMode503(logging.Filter):
    """Filters out 503 errors if maintenance mode is activated."""
    def filter(self, record):
        """Return False if maintenance mode is on and the given record has a status code of 503."""
        return not (settings.MAINTENANCE_MODE and getattr(record, 'status_code', None) == 503)

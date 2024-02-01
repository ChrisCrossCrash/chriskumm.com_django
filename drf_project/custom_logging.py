# Custom Logging Configuration
# https://docs.djangoproject.com/en/5.0/topics/logging/#module-django.utils.log

CUSTOM_LOGGING = {
    "version": 1,
    # Disabling existing loggers is not the same as removing them. That is why, rather
    # than setting disable_existing_loggers to True, we set it to False and set
    # LOGGING_CONFIG to None in settings.py. Then we load this logging configuration
    # with logging.config.dictConfig(CUSTOM_LOGGING) in settings.py.
    # https://docs.djangoproject.com/en/5.0/topics/logging/#configuring-logging
    "disable_existing_loggers": False,
    # A filter is used to provide additional control over which log records are passed
    # from logger to handler.
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    # Ultimately, a log record needs to be rendered as text. Formatters describe the
    # exact format of that text. A formatter usually consists of a Python formatting
    # string containing LogRecord attributes; however, you can also write custom
    # formatters to implement specific formatting behavior.
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    # The handler is the engine that determines what happens to each message in a
    # logger. It describes a particular logging behavior, such as writing a message to
    # the screen, to a file, or to a network socket.
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": [
                "require_debug_false",
            ],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    # A logger is the entry point into the logging system. Each logger is a named
    # bucket to which messages can be written for processing.
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "core": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "ai_pals": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

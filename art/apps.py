from django.apps import AppConfig


class ArtConfig(AppConfig):
    name = "art"

    def ready(self):
        # The art.signals module needs to get imported into Django somewhere.
        # The Django docs says that this is the best place for it.
        # https://docs.djangoproject.com/en/3.2/topics/signals/#connecting-receiver-functions
        import art.signals

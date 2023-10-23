from django.db import models
from solo.models import SingletonModel


class SystemMessage(SingletonModel):
    content = models.TextField()

    def __str__(self):
        return "System Message"

    class Meta:
        verbose_name = "System Message"

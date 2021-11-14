from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Piece


@receiver(post_save, sender=Piece)
def save_base64_thumbnail(**kwargs):
    update_fields = kwargs["update_fields"]

    # Without this, the signal will be called in an infinite loop.
    if update_fields is not None and "image_b64_thumbnail" in update_fields:
        return

    piece = kwargs["instance"]
    b64thumb = piece.generate_base64_data_thumbnail()
    piece.image_b64_thumbnail = b64thumb
    piece.save(update_fields=["image_b64_thumbnail"])

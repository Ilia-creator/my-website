from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from game.models import PlayerProgress

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_player_progress(sender, instance, created, **kwargs):
    if created:
        PlayerProgress.objects.create(user=instance)

from .models import ELORated
from django.db.models.signals import post_save
from django.dispatch import receiver
from ._django_settings import DjangoSettings


@receiver(post_save)
def create_or_update_user_papers_checking(sender, instance, created, **kwargs):
    settings = DjangoSettings()
    senderName = sender.__name__.lower()

    if senderName not in settings.get_rated_models():
        return None

    if created:
        ELORated.objects.create(
            content_object = instance,
            object_id      = instance.pk
        )

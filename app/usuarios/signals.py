from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from gestao_riscos.auth import sync_user_with_profile

from .models import Usuario


@receiver(post_save, sender=Usuario, dispatch_uid="usuarios_sync_auth_user_from_profile")
def sync_auth_user_from_profile(sender, instance, created, **kwargs):
    _ = sender, created, kwargs
    matricula = (instance.matricula or "").strip()
    if not matricula:
        return

    user_model = get_user_model()
    user = user_model.objects.filter(username__iexact=matricula).first()
    if user is None:
        user = user_model(username=matricula)
        user.set_unusable_password()

    sync_user_with_profile(user, usuario=instance)
    user.save()

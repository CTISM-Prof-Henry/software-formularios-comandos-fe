from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from gestao_riscos.auth import sync_user_with_profile

from .models import Usuario


@receiver(post_save, sender=Usuario, dispatch_uid="usuarios_sync_auth_user_from_profile")
def sync_auth_user_from_profile(sender, instance, **kwargs):
    matricula = (instance.matricula or "").strip()
    if not matricula:
        return

    user_model = get_user_model()
    user = user_model._default_manager.filter(username__iexact=matricula).first()
    if user is None:
        return

    sync_user_with_profile(user, usuario=instance)
    user.save(
        update_fields=[
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "is_active",
        ]
    )

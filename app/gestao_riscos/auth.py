from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from usuarios.models import PerfilAcesso, Usuario


class _NoRedirectHandler(HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return fp

    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    http_error_308 = http_error_302


def split_full_name(full_name):
    normalized = (full_name or "").strip()
    if not normalized:
        return "", ""

    parts = normalized.split(None, 1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


def validate_library_credentials(username, password):
    payload = urlencode(
        {
            "j_username": username,
            "j_password": password,
            "enter": "",
        }
    ).encode("utf-8")

    request = Request(
        settings.UFSM_LIBRARY_AUTH_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    opener = build_opener(_NoRedirectHandler)

    try:
        with opener.open(request, timeout=settings.UFSM_LIBRARY_AUTH_TIMEOUT) as response:
            return response.status == 302
    except HTTPError as exc:
        return exc.code == 302
    except (TimeoutError, URLError):
        return False


def sync_user_with_profile(user, usuario=None):
    usuario = usuario or Usuario.objects.filter(matricula__iexact=user.username).first()

    if usuario:
        user.username = usuario.matricula or user.username
        email = usuario.email or f"{user.username}@ufsm.br"
        full_name = usuario.nome or user.username
        is_admin = usuario.perfil_acesso == PerfilAcesso.ADMIN
    else:
        email = user.email or f"{user.username}@ufsm.br"
        full_name = user.get_full_name() or user.username
        is_admin = user.is_superuser or user.is_staff

    first_name, last_name = split_full_name(full_name)

    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.is_staff = is_admin
    user.is_superuser = is_admin
    user.is_active = True

    return user


class LibraryAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, auth_source=None, **kwargs):
        if auth_source != "ufsm" or not username or not password:
            return None

        if not validate_library_credentials(username, password):
            return None

        user_model = get_user_model()
        user = user_model._default_manager.filter(username__iexact=username).first()
        created = user is None

        if created:
            user = user_model(username=username)
            user.set_unusable_password()
        elif user.username != username:
            user.username = username

        sync_user_with_profile(user)
        user.save()
        return user

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model._default_manager.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

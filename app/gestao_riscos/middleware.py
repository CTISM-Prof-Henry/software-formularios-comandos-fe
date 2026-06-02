from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from .permissions import build_permissions_context, can_access_risk_module
from .user_context import (
    clear_current_request,
    get_usuario_for_django_user,
    needs_profile_update,
    set_current_request,
)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)
        request.current_usuario = get_usuario_for_django_user(
            request.user,
            select_related_unidade=True,
        )
        request.perms_context = build_permissions_context(
            request.user,
            usuario=request.current_usuario,
        )
        try:
            return self._handle_request(request)
        finally:
            clear_current_request()

    def _handle_request(self, request):
        if self._requires_login(request):
            login_url = reverse("login")
            return redirect(f"{login_url}?next={request.get_full_path()}")

        if self._requires_profile_update(request):
            return redirect("atualizar-cadastro")

        if self._requires_role(request):
            return redirect("sem-permissao")

        return self.get_response(request)

    def _requires_login(self, request):
        if request.user.is_authenticated:
            return False

        public_paths = (
            reverse("login"),
            reverse("local-registration"),
            reverse("healthcheck"),
            f"/{settings.STATIC_URL.lstrip('/')}",
        )
        return not self._is_public_path(request.path, public_paths)

    def _requires_role(self, request):
        if not request.user.is_authenticated:
            return False

        public_paths = (
            reverse("login"),
            reverse("local-registration"),
            reverse("healthcheck"),
            reverse("sem-permissao"),
            reverse("atualizar-cadastro"),
            "/logout/",
            f"/{settings.STATIC_URL.lstrip('/')}",
        )
        if self._is_public_path(request.path, public_paths):
            return False

        return not can_access_risk_module(request.user, usuario=request.current_usuario)

    def _requires_profile_update(self, request):
        if not request.user.is_authenticated:
            return False

        public_paths = (
            reverse("login"),
            reverse("local-registration"),
            reverse("healthcheck"),
            reverse("atualizar-cadastro"),
            "/logout/",
            f"/{settings.STATIC_URL.lstrip('/')}",
        )
        if self._is_public_path(request.path, public_paths):
            return False

        return needs_profile_update(request.user, usuario=request.current_usuario)

    @staticmethod
    def _is_public_path(path, public_paths):
        if path == "/admin" or path.startswith("/admin/"):
            return True
        return path.startswith(public_paths)

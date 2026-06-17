from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from .user_context import get_usuario_for_django_user


ADMIN_ROLE = "admin"
GESTAO_RISCOS_ROLE = "gestao-riscos"


def has_role(user, role, usuario=None):
    if not user.is_authenticated:
        return False

    usuario = usuario or get_usuario_for_django_user(user)
    if usuario:
        return _has_local_profile_role(user, role, usuario=usuario)

    return user.is_superuser or user.groups.filter(name=role).exists()


def is_admin(user, usuario=None):
    return has_role(user, ADMIN_ROLE, usuario=usuario)


def is_risk_manager(user, usuario=None):
    return not is_admin(user, usuario=usuario) and has_role(
        user,
        GESTAO_RISCOS_ROLE,
        usuario=usuario,
    )


def can_access_risk_module(user, usuario=None):
    return is_admin(user, usuario=usuario) or is_risk_manager(user, usuario=usuario)


def build_permissions_context(user, usuario=None):
    return {
        "is_admin": is_admin(user, usuario=usuario),
        "is_risk_manager": is_risk_manager(user, usuario=usuario),
        "can_access_risks": can_access_risk_module(user, usuario=usuario),
    }


class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = ()

    def test_func(self):
        user = self.request.user
        return any(has_role(user, role) for role in self.required_roles)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect("sem-permissao")
        return super().handle_no_permission()


class AdminRequiredMixin(RoleRequiredMixin):
    required_roles = (ADMIN_ROLE,)


class RiskModuleRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return can_access_risk_module(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect("sem-permissao")
        return super().handle_no_permission()


def _has_local_profile_role(_user, role, usuario=None):
    from usuarios.models import PerfilAcesso

    if not usuario:
        return False

    if role == ADMIN_ROLE:
        return usuario.perfil_acesso == PerfilAcesso.ADMIN
    if role == GESTAO_RISCOS_ROLE:
        return usuario.perfil_acesso == PerfilAcesso.GESTAO_RISCOS
    return False

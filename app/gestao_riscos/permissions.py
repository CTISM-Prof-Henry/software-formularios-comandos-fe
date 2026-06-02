from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from .user_context import get_usuario_for_django_user


ADMIN_ROLE = "admin"
GESTAO_RISCOS_ROLE = "gestao-riscos"


def has_role(user, role, usuario=None):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.groups.filter(name=role).exists():
        return True
    return _has_local_profile_role(user, role, usuario=usuario)


def is_admin(user, usuario=None):
    return has_role(user, ADMIN_ROLE, usuario=usuario)


def is_risk_manager(user, usuario=None):
    return not is_admin(user, usuario=usuario) and has_role(
        user,
        GESTAO_RISCOS_ROLE,
        usuario=usuario,
    )


def can_access_risk_module(user, usuario=None):
    return is_admin(user, usuario=usuario) or has_role(
        user,
        GESTAO_RISCOS_ROLE,
        usuario=usuario,
    )


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


class RiskModuleRequiredMixin(RoleRequiredMixin):
    required_roles = (ADMIN_ROLE, GESTAO_RISCOS_ROLE)


def _has_local_profile_role(user, role, usuario=None):
    from usuarios.models import PerfilAcesso

    usuario = usuario or get_usuario_for_django_user(user)
    if not usuario:
        return False

    if role == ADMIN_ROLE:
        return usuario.perfil_acesso == PerfilAcesso.ADMIN
    if role == GESTAO_RISCOS_ROLE:
        return usuario.perfil_acesso == PerfilAcesso.GESTAO_RISCOS
    return False

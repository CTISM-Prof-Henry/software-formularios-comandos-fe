from threading import local

from usuarios.models import Usuario

_state = local()


def set_current_request(request):
    _state.request = request


def clear_current_request():
    _state.request = None


def get_current_request():
    return getattr(_state, "request", None)


def get_usuario_for_django_user(user, *, select_related_unidade=False):
    if not user.is_authenticated:
        return None

    queryset = Usuario.objects
    if select_related_unidade:
        queryset = queryset.select_related("unidade")

    if user.email:
        usuario = queryset.filter(email__iexact=user.email).first()
        if usuario:
            return usuario

    if user.username:
        return queryset.filter(matricula__iexact=user.username).first()

    return None


def needs_profile_update(user, usuario=None):
    if user.is_superuser:
        return False

    usuario = usuario or get_usuario_for_django_user(user)
    return usuario is None or not usuario.senha_local_definida

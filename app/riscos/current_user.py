from django.conf import settings

from gestao_riscos.user_context import get_current_request, get_usuario_for_django_user
from unidades.models import Unidade
from usuarios.models import Usuario

CURRENT_USER_NAME = "Fulano"
CURRENT_USER_DEPARTMENT_NAME = "Politécnico"


def get_current_user():
    request = get_current_request()
    if request and request.user.is_authenticated:
        usuario = getattr(request, "current_usuario", None)
        if usuario is None:
            usuario = get_usuario_for_django_user(
                request.user,
                select_related_unidade=True,
            )
        if usuario:
            return usuario

    simulated_user_email = getattr(settings, "SIMULATED_USER_EMAIL", "")
    return (
        Usuario.objects.select_related("unidade")
        .filter(email__iexact=simulated_user_email)
        .first()
        or Usuario.objects.select_related("unidade")
        .filter(nome__iexact=CURRENT_USER_NAME)
        .first()
    )


def get_current_user_name():
    request = get_current_request()
    if request and request.user.is_authenticated:
        full_name = request.user.get_full_name()
        if full_name:
            return full_name
        if request.user.username:
            return request.user.username

    usuario = get_current_user()
    if usuario and usuario.nome:
        return usuario.nome
    return CURRENT_USER_NAME


def get_current_user_department():
    usuario = get_current_user()
    if usuario and usuario.unidade:
        return usuario.unidade
    return None


def get_current_user_units():
    departamento = get_current_user_department()
    if not departamento:
        return Unidade.objects.none()
    return Unidade.objects.filter(id__in=get_current_user_unit_ids())


def get_current_user_unit_ids():
    departamento = get_current_user_department()
    if not departamento:
        return []

    unidade_ids = [departamento.id]
    visitadas = {departamento.id}
    pendentes = [departamento.id]

    while pendentes:
        filhas_ids = list(
            Unidade.objects.filter(unidade_pai_id__in=pendentes).values_list("id", flat=True)
        )
        novas_ids = [unidade_id for unidade_id in filhas_ids if unidade_id not in visitadas]
        unidade_ids.extend(novas_ids)
        visitadas.update(novas_ids)
        pendentes = novas_ids

    return unidade_ids


def user_can_manage_risco(risco):
    return risco.unidade_id in get_current_user_unit_ids()


def _get_default_department():
    return (
        Unidade.objects.filter(sigla__iexact="POLITECNICO").first()
        or Unidade.objects.filter(sigla__iexact="POLI").first()
        or Unidade.objects.filter(nome__icontains="Politécnico").first()
        or Unidade.objects.filter(nome__icontains="Politecnico").first()
        or Unidade.objects.filter(nome__icontains=CURRENT_USER_DEPARTMENT_NAME).first()
    )

from django.conf import settings

from unidades.models import Unidade
from usuarios.models import Usuario

CURRENT_USER_NAME = "Fulano"
CURRENT_USER_DEPARTMENT_NAME = "Politecnico"


def get_current_user():
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
    usuario = get_current_user()
    if usuario and usuario.nome:
        return usuario.nome
    return CURRENT_USER_NAME


def get_current_user_department():
    usuario = get_current_user()
    if usuario and usuario.unidade:
        return usuario.unidade
    return (
        Unidade.objects.filter(sigla__iexact="POLITECNICO").first()
        or Unidade.objects.filter(sigla__iexact="POLI").first()
        or Unidade.objects.filter(nome__icontains=CURRENT_USER_DEPARTMENT_NAME).first()
    )


def get_current_user_units():
    departamento = get_current_user_department()
    if not departamento:
        return Unidade.objects.none()

    unidades_ids = [departamento.id]
    unidades_vistas = {departamento.id}
    pendentes = [departamento.id]

    while pendentes:
        filhas_ids = list(
            Unidade.objects.filter(unidade_pai_id__in=pendentes).values_list("id", flat=True)
        )
        novas_ids = [unidade_id for unidade_id in filhas_ids if unidade_id not in unidades_vistas]
        unidades_ids.extend(novas_ids)
        unidades_vistas.update(novas_ids)
        pendentes = novas_ids

    return Unidade.objects.filter(id__in=unidades_ids).order_by("sigla")


def user_can_manage_risco(risco):
    departamento = get_current_user_department()
    if not departamento:
        return False

    unidade = risco.unidade
    while unidade:
        if unidade == departamento:
            return True
        unidade = unidade.unidade_pai
    return False

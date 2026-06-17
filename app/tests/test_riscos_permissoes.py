from datetime import date
from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from riscos.models import (
    AcaoTratamento,
    Desafio,
    EficaciaControle,
    Macroprocesso,
    Objetivo,
    RespostaRisco,
    Risco,
    SituacaoTratamento,
    TipoRisco,
)
from unidades.models import TipoUnidade, Unidade
from usuarios.models import PerfilAcesso, Usuario


@pytest.fixture(name="cenario_riscos")
def criar_cenario_riscos(db):
    _ = db
    sufixo = uuid4().hex[:8]
    unidade_usuario = Unidade.objects.create(
        sigla=f"UA{sufixo[:5]}",
        nome="Unidade do Usuário",
        tipo_unidade=TipoUnidade.DIRETORIA,
    )
    unidade_filha = Unidade.objects.create(
        sigla=f"UF{sufixo[:5]}",
        nome="Unidade Filha",
        tipo_unidade=TipoUnidade.COORDENACAO,
        unidade_pai=unidade_usuario,
    )
    outra_unidade = Unidade.objects.create(
        sigla=f"OU{sufixo[:5]}",
        nome="Outra Unidade",
        tipo_unidade=TipoUnidade.DIRETORIA,
    )
    desafio = Desafio.objects.create(codigo=f"D{sufixo}", nome="Desafio")
    objetivo = Objetivo.objects.create(
        desafio=desafio,
        codigo=f"O{sufixo}",
        descricao="Objetivo",
    )
    macroprocesso = Macroprocesso.objects.create(nome=f"Macroprocesso {sufixo}")
    dados_base = {
        "tipo_risco": TipoRisco.OPERACIONAL,
        "desafio": desafio,
        "objetivo": objetivo,
        "macroprocesso": macroprocesso,
        "probabilidade": 2,
        "impacto": 2,
        "eficacia_controles": EficaciaControle.MEDIANA,
        "resposta": RespostaRisco.MITIGAR,
        "acao": AcaoTratamento.PREVENTIVA,
        "data_inicio": date(2026, 1, 1),
        "data_fim": date(2026, 1, 31),
        "situacao": SituacaoTratamento.NAO_INICIADO,
    }
    risco_proprio = Risco.objects.create(
        **dados_base,
        unidade=unidade_usuario,
        risco_identificado="Risco da própria unidade",
    )
    risco_filha = Risco.objects.create(
        **dados_base,
        unidade=unidade_filha,
        risco_identificado="Risco da unidade filha",
    )
    risco_outra_unidade = Risco.objects.create(
        **dados_base,
        unidade=outra_unidade,
        risco_identificado="Risco de outra unidade",
    )
    return {
        "unidade_usuario": unidade_usuario,
        "unidade_filha": unidade_filha,
        "outra_unidade": outra_unidade,
        "risco_proprio": risco_proprio,
        "risco_filha": risco_filha,
        "risco_outra_unidade": risco_outra_unidade,
        "dados_post": {
            **dados_base,
            "risco_identificado": "Risco criado pelo usuário",
        },
    }


def criar_usuario_logado(
    client,
    unidade,
    matricula,
    perfil_acesso=PerfilAcesso.GESTAO_RISCOS,
):
    user = get_user_model().objects.create_user(
        username=matricula,
        password="senha-teste",
        first_name="Usuário",
        last_name="Teste",
    )
    Usuario.objects.create(
        unidade=unidade,
        matricula=matricula,
        nome=f"Usuário {matricula}",
        email=f"{matricula}@example.com",
        perfil_acesso=perfil_acesso,
        senha_local_definida=True,
    )
    client.force_login(user)
    return client


@pytest.fixture(name="cliente_gestao")
def criar_cliente_gestao(client, cenario_riscos):
    return criar_usuario_logado(client, cenario_riscos["unidade_usuario"], "gestao")


@pytest.mark.django_db
def test_usuario_com_gestao_visualiza_inicio_e_riscos(
    cliente_gestao,
    cenario_riscos,
):
    inicio_response = cliente_gestao.get(reverse("index"))
    riscos_response = cliente_gestao.get(reverse("risco-list"))

    assert inicio_response.status_code == 200
    assert riscos_response.status_code == 200
    assert "Risco da própria" in riscos_response.content.decode()
    assert "Risco da unidade" in riscos_response.content.decode()
    assert "Risco de outra" in riscos_response.content.decode()
    assert reverse(
        "risco-update",
        kwargs={"pk": cenario_riscos["risco_proprio"].pk},
    ) in riscos_response.content.decode()
    assert reverse(
        "risco-update",
        kwargs={"pk": cenario_riscos["risco_filha"].pk},
    ) in riscos_response.content.decode()
    assert reverse(
        "risco-update",
        kwargs={"pk": cenario_riscos["risco_outra_unidade"].pk},
    ) not in riscos_response.content.decode()


@pytest.mark.django_db
def test_usuario_sem_gestao_visualiza_inicio_mas_nao_riscos(client, cenario_riscos):
    cliente_sem_acesso = criar_usuario_logado(
        client,
        cenario_riscos["unidade_usuario"],
        "sem-acesso-riscos",
        perfil_acesso=PerfilAcesso.ESTUDANTE,
    )

    inicio_response = cliente_sem_acesso.get(reverse("index"))
    riscos_response = cliente_sem_acesso.get(reverse("risco-list"))

    assert inicio_response.status_code == 200
    assert riscos_response.status_code == 302
    assert riscos_response.url == reverse("sem-permissao")


@pytest.mark.django_db
def test_usuario_visualiza_impressao_de_outra_unidade_mas_nao_edita(
    cliente_gestao,
    cenario_riscos,
):
    risco_outra_unidade = cenario_riscos["risco_outra_unidade"]

    print_response = cliente_gestao.get(
        reverse("risco-print", kwargs={"pk": risco_outra_unidade.pk})
    )
    edit_response = cliente_gestao.get(
        reverse("risco-update", kwargs={"pk": risco_outra_unidade.pk})
    )

    assert print_response.status_code == 200
    assert edit_response.status_code == 403


@pytest.mark.django_db
def test_unidade_pai_pode_criar_risco_para_unidade_filha(
    cliente_gestao,
    cenario_riscos,
):
    dados_post = {
        "unidade": cenario_riscos["unidade_filha"].pk,
        "tipo_risco": cenario_riscos["dados_post"]["tipo_risco"],
        "desafio": cenario_riscos["dados_post"]["desafio"].pk,
        "objetivo": cenario_riscos["dados_post"]["objetivo"].pk,
        "macroprocesso": cenario_riscos["dados_post"]["macroprocesso"].pk,
        "risco_identificado": cenario_riscos["dados_post"]["risco_identificado"],
        "probabilidade": cenario_riscos["dados_post"]["probabilidade"],
        "impacto": cenario_riscos["dados_post"]["impacto"],
        "eficacia_controles": cenario_riscos["dados_post"]["eficacia_controles"],
        "resposta": cenario_riscos["dados_post"]["resposta"],
        "acao": cenario_riscos["dados_post"]["acao"],
        "data_inicio": cenario_riscos["dados_post"]["data_inicio"],
        "data_fim": cenario_riscos["dados_post"]["data_fim"],
        "situacao": cenario_riscos["dados_post"]["situacao"],
    }

    response = cliente_gestao.post(reverse("risco-create"), dados_post)

    assert response.status_code == 302
    assert Risco.objects.filter(
        unidade=cenario_riscos["unidade_filha"],
        risco_identificado="Risco criado pelo usuário",
    ).exists()


@pytest.mark.django_db
def test_usuario_cria_risco_apenas_para_sua_unidade_ou_filhas(
    cliente_gestao,
    cenario_riscos,
):
    dados_post = {
        "unidade": cenario_riscos["outra_unidade"].pk,
        "tipo_risco": cenario_riscos["dados_post"]["tipo_risco"],
        "desafio": cenario_riscos["dados_post"]["desafio"].pk,
        "objetivo": cenario_riscos["dados_post"]["objetivo"].pk,
        "macroprocesso": cenario_riscos["dados_post"]["macroprocesso"].pk,
        "risco_identificado": cenario_riscos["dados_post"]["risco_identificado"],
        "probabilidade": cenario_riscos["dados_post"]["probabilidade"],
        "impacto": cenario_riscos["dados_post"]["impacto"],
        "eficacia_controles": cenario_riscos["dados_post"]["eficacia_controles"],
        "resposta": cenario_riscos["dados_post"]["resposta"],
        "acao": cenario_riscos["dados_post"]["acao"],
        "data_inicio": cenario_riscos["dados_post"]["data_inicio"],
        "data_fim": cenario_riscos["dados_post"]["data_fim"],
        "situacao": cenario_riscos["dados_post"]["situacao"],
    }

    response = cliente_gestao.post(reverse("risco-create"), dados_post)

    assert response.status_code == 200
    assert not Risco.objects.filter(
        unidade=cenario_riscos["outra_unidade"],
        risco_identificado="Risco criado pelo usuário",
    ).exists()


@pytest.mark.django_db
def test_unidade_filha_nao_edita_risco_da_unidade_pai(client, cenario_riscos):
    cliente_filha = criar_usuario_logado(client, cenario_riscos["unidade_filha"], "filha")

    edit_response = cliente_filha.get(
        reverse("risco-update", kwargs={"pk": cenario_riscos["risco_proprio"].pk})
    )
    filha_response = cliente_filha.get(
        reverse("risco-update", kwargs={"pk": cenario_riscos["risco_filha"].pk})
    )

    assert edit_response.status_code == 403
    assert filha_response.status_code == 200

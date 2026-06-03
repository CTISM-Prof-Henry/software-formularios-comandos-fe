import pytest
from django.urls import reverse

from unidades.models import TipoUnidade, Unidade
from usuarios.models import PerfilAcesso, Usuario


@pytest.fixture(name="unidade_teste")
def criar_unidade_teste(db):
    _ = db
    return Unidade.objects.create(
        sigla="POLI",
        nome="Politecnico",
        tipo_unidade=TipoUnidade.DIRETORIA,
    )


@pytest.mark.django_db
def test_deve_listar_usuarios_quando_acessar_rota_sem_login(client, unidade_teste):
    Usuario.objects.create(
        unidade=unidade_teste,
        matricula="2024001",
        nome="Aluno Teste",
        email="aluno.teste@ufsm.br",
        perfil_acesso=PerfilAcesso.ESTUDANTE,
    )

    response = client.get(reverse("usuario-list"))

    assert response.status_code == 200
    assert "Aluno Teste" in response.content.decode()


@pytest.mark.django_db
def test_deve_criar_usuario_quando_enviar_dados_validos_no_crud(client, unidade_teste):
    response = client.post(
        reverse("usuario-create"),
        {
            "unidade": unidade_teste.pk,
            "matricula": "2024002",
            "nome": "Novo Usuario",
            "email": "novo.usuario@ufsm.br",
            "perfil_acesso": PerfilAcesso.ADMIN,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("usuario-list")
    assert Usuario.objects.filter(matricula="2024002").exists()


@pytest.mark.django_db
def test_deve_abrir_pagina_inicial_quando_acessar_raiz_sem_login(client):
    response = client.get(reverse("index"))

    assert response.status_code == 200
    assert "Comandos FE" in response.content.decode()


@pytest.mark.django_db
def test_deve_exibir_usuario_na_listagem_quando_criado_com_dados_validos(client):
    unidade = Unidade.objects.create(
        sigla="CAL",
        nome="Centro de Artes e Letras",
        tipo_unidade=TipoUnidade.DIRETORIA,
    )

    create_response = client.post(
        reverse("usuario-create"),
        {
            "unidade": unidade.pk,
            "matricula": "2024999",
            "nome": "Integracao Usuario",
            "email": "integracao.usuario@ufsm.br",
            "perfil_acesso": PerfilAcesso.ADMIN,
        },
    )

    assert create_response.status_code == 302
    assert create_response.url == reverse("usuario-list")

    list_response = client.get(reverse("usuario-list"))

    assert list_response.status_code == 200
    assert "Integracao Usuario" in list_response.content.decode()
    assert "2024999" in list_response.content.decode()
    assert Usuario.objects.filter(
        matricula="2024999",
        unidade=unidade,
        perfil_acesso=PerfilAcesso.ADMIN,
    ).exists()

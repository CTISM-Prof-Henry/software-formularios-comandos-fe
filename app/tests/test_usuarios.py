import pytest
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.urls import reverse

from unidades.models import TipoUnidade, Unidade
from usuarios.models import PerfilAcesso, Usuario


@pytest.fixture(name="unidade_teste")
def criar_unidade_teste(db):
    _ = db
    unidade, _created = Unidade.objects.get_or_create(
        sigla="POLI",
        defaults={
            "nome": "Politécnico",
            "tipo_unidade": TipoUnidade.DIRETORIA,
        },
    )
    return unidade


@pytest.fixture(name="admin_logado")
def criar_admin_logado(client, unidade_teste):
    user = get_user_model().objects.create_user(
        username="admin",
        password="senha-teste",
        first_name="Admin",
        last_name="Teste",
    )
    Usuario.objects.create(
        unidade=unidade_teste,
        matricula="admin",
        nome="Admin Teste",
        email="admin.teste@ufsm.br",
        perfil_acesso=PerfilAcesso.ADMIN,
    )
    client.force_login(user)
    return user


@pytest.mark.django_db
def test_deve_listar_usuarios_quando_acessar_rota_com_admin(
    client,
    unidade_teste,
    admin_logado,
):
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
def test_deve_criar_usuario_quando_enviar_dados_validos_no_crud(
    client,
    unidade_teste,
    admin_logado,
):
    response = client.post(
        reverse("usuario-create"),
        {
            "unidade": unidade_teste.pk,
            "matricula": "2024002",
            "nome": "Novo Usuário",
            "email": "novo.usuario@ufsm.br",
            "perfil_acesso": PerfilAcesso.ADMIN,
            "senha": "senha-teste-123",
            "confirmar_senha": "senha-teste-123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("usuario-list")
    assert Usuario.objects.filter(matricula="2024002").exists()
    assert authenticate(username="2024002", password="senha-teste-123") is not None


@pytest.mark.django_db
def test_edicao_de_usuario_mostra_botao_resetar_senha_sem_campos_de_senha(
    client,
    unidade_teste,
    admin_logado,
):
    usuario = Usuario.objects.create(
        unidade=unidade_teste,
        matricula="2024003",
        nome="Usuário Editável",
        email="usuario.editavel@ufsm.br",
        perfil_acesso=PerfilAcesso.ESTUDANTE,
    )

    response = client.get(reverse("usuario-update", kwargs={"pk": usuario.pk}))
    html = response.content.decode()

    assert response.status_code == 200
    assert "Resetar senha" in html
    assert reverse("usuario-reset-password", kwargs={"pk": usuario.pk}) in html
    assert "Nova senha" not in html
    assert "Confirmar nova senha" not in html


@pytest.mark.django_db
def test_deve_resetar_senha_do_usuario_pelo_crud(
    client,
    unidade_teste,
    admin_logado,
):
    usuario = Usuario.objects.create(
        unidade=unidade_teste,
        matricula="2024004",
        nome="Usuário Reset",
        email="usuario.reset@ufsm.br",
        perfil_acesso=PerfilAcesso.ESTUDANTE,
    )

    response = client.post(
        reverse("usuario-reset-password", kwargs={"pk": usuario.pk}),
        {
            "senha": "senha-nova-123",
            "confirmar_senha": "senha-nova-123",
        },
    )

    usuario.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("usuario-list")
    assert usuario.senha_local_definida is True
    assert authenticate(username="2024004", password="senha-nova-123") is not None


@pytest.mark.django_db
def test_usuario_criado_direto_ganha_conta_local_e_pode_resetar_senha(
    client,
    unidade_teste,
    admin_logado,
):
    usuario = Usuario.objects.create(
        unidade=unidade_teste,
        matricula="2024005",
        nome="Usuário Admin Django",
        email="usuario.admin.django@ufsm.br",
        perfil_acesso=PerfilAcesso.ESTUDANTE,
    )
    django_user = get_user_model().objects.get(username="2024005")

    assert django_user.has_usable_password() is False
    assert authenticate(username="2024005", password="senha-nova-123") is None

    response = client.post(
        reverse("usuario-reset-password", kwargs={"pk": usuario.pk}),
        {
            "senha": "senha-nova-123",
            "confirmar_senha": "senha-nova-123",
        },
    )

    assert response.status_code == 302
    assert authenticate(username="2024005", password="senha-nova-123") is not None


@pytest.mark.django_db
def test_usuario_editado_para_sem_acesso_perde_permissao_admin(
    client,
    unidade_teste,
):
    django_user = get_user_model().objects.create_user(
        username="ex-admin",
        password="senha-teste",
        is_staff=True,
        is_superuser=True,
    )
    usuario = Usuario.objects.create(
        unidade=unidade_teste,
        matricula="ex-admin",
        nome="Ex Admin",
        email="ex.admin@ufsm.br",
        perfil_acesso=PerfilAcesso.ADMIN,
        senha_local_definida=True,
    )
    usuario.perfil_acesso = PerfilAcesso.ESTUDANTE
    usuario.save()

    django_user.refresh_from_db()
    client.force_login(django_user)

    assert django_user.is_staff is False
    assert django_user.is_superuser is False
    assert client.get(reverse("index")).status_code == 200
    assert client.get(reverse("risco-list")).status_code == 302
    assert client.get(reverse("usuario-list")).status_code == 302


@pytest.mark.django_db
def test_deve_abrir_pagina_inicial_quando_acessar_raiz_sem_login(client):
    response = client.get(reverse("index"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_deve_exibir_usuario_na_listagem_quando_criado_com_dados_validos(
    client,
    admin_logado,
):
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
            "nome": "Integração Usuário",
            "email": "integracao.usuario@ufsm.br",
            "perfil_acesso": PerfilAcesso.ADMIN,
            "senha": "senha-teste-123",
            "confirmar_senha": "senha-teste-123",
        },
    )

    assert create_response.status_code == 302
    assert create_response.url == reverse("usuario-list")

    list_response = client.get(reverse("usuario-list"))

    assert list_response.status_code == 200
    assert "Integração Usuário" in list_response.content.decode()
    assert "2024999" in list_response.content.decode()
    assert Usuario.objects.filter(
        matricula="2024999",
        unidade=unidade,
        perfil_acesso=PerfilAcesso.ADMIN,
    ).exists()

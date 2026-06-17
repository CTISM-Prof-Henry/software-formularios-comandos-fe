import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from unidades.forms import UnidadeForm
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
        username="admin-unidades",
        password="senha-teste",
        first_name="Admin",
        last_name="Unidades",
    )
    Usuario.objects.create(
        unidade=unidade_teste,
        matricula="admin-unidades",
        nome="Admin Unidades",
        email="admin.unidades@ufsm.br",
        perfil_acesso=PerfilAcesso.ADMIN,
    )
    client.force_login(user)
    return user


@pytest.mark.django_db
def test_str_retorna_sigla_e_nome_da_unidade():
    unidade = Unidade(
        sigla="CT",
        nome="Centro de Tecnologia",
        tipo_unidade=TipoUnidade.DIRETORIA,
    )
    assert str(unidade) == "CT - Centro de Tecnologia"


def test_formulario_exige_sigla_nome_e_tipo():
    form = UnidadeForm(data={"sigla": "", "nome": "", "tipo_unidade": ""})

    assert form.is_valid() is False
    assert "sigla" in form.errors
    assert "nome" in form.errors
    assert "tipo_unidade" in form.errors


@pytest.mark.django_db
def test_listagem_exibe_unidades_cadastradas(client, admin_logado):
    _ = admin_logado
    Unidade.objects.create(
        sigla="PROPLAN",
        nome="Pro-Reitoria de Planejamento",
        tipo_unidade=TipoUnidade.DIRETORIA,
    )

    response = client.get(reverse("unidade-list"))

    assert response.status_code == 200
    assert "PROPLAN" in response.content.decode()
    assert "Pro-Reitoria de Planejamento" in response.content.decode()


@pytest.mark.django_db
def test_cria_nova_unidade_com_sucesso(client, admin_logado):
    _ = admin_logado
    dados_da_requisicao = {
        "sigla": "CCSH",
        "nome": "Centro de Ciencias Sociais e Humanas",
        "tipo_unidade": TipoUnidade.DIRETORIA,
    }

    response = client.post(reverse("unidade-create"), data=dados_da_requisicao)

    assert response.status_code == 302
    assert Unidade.objects.filter(sigla="CCSH").exists()


@pytest.mark.django_db
def test_recusa_dados_invalidos(client, admin_logado):
    _ = admin_logado
    dados_invalidos = {"sigla": "", "nome": "", "tipo_unidade": ""}

    response = client.post(reverse("unidade-create"), data=dados_invalidos)

    assert response.status_code == 200
    assert Unidade.objects.filter(sigla="").exists() is False

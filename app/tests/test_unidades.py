import pytest
from django.urls import reverse
from unidades.forms import UnidadeForm
from unidades.models import TipoUnidade, Unidade

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
def test_listagem_exibe_unidades_cadastradas(client):
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
def test_cria_nova_unidade_com_sucesso(client):
    dados_da_requisicao = {
        "sigla": "CCSH",
        "nome": "Centro de Ciências Sociais e Humanas",
        "tipo_unidade": TipoUnidade.DIRETORIA,
    }

    response = client.post(reverse("unidade-create"), data=dados_da_requisicao)

    assert response.status_code == 302
    assert Unidade.objects.filter(sigla="CCSH").exists()


@pytest.mark.django_db
def test_recusa_dados_invalidos(client):
    dados_invalidos = {"sigla": "", "nome": "", "tipo_unidade": ""}

    response = client.post(reverse("unidade-create"), data=dados_invalidos)

    assert response.status_code == 200
    assert Unidade.objects.filter(sigla="").exists() is False

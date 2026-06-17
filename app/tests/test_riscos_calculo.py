from datetime import date
from uuid import uuid4

import pytest

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


@pytest.fixture(name="dados_risco")
def criar_dados_risco(db):
    _ = db
    sufixo = uuid4().hex[:8]
    unidade = Unidade.objects.create(
        sigla=f"PR{sufixo[:6]}",
        nome="Politécnico Riscos",
        tipo_unidade=TipoUnidade.DIRETORIA,
    )
    desafio = Desafio.objects.create(codigo=f"D{sufixo[:8]}", nome="Desafio")
    objetivo = Objetivo.objects.create(
        desafio=desafio,
        codigo=f"O{sufixo[:8]}",
        descricao="Objetivo",
    )
    macroprocesso = Macroprocesso.objects.create(nome=f"Macroprocesso {sufixo}")
    return {
        "unidade": unidade,
        "tipo_risco": TipoRisco.OPERACIONAL,
        "desafio": desafio,
        "objetivo": objetivo,
        "macroprocesso": macroprocesso,
        "risco_identificado": "Risco de teste",
        "probabilidade": 4,
        "impacto": 5,
        "resposta": RespostaRisco.MITIGAR,
        "acao": AcaoTratamento.PREVENTIVA,
        "data_inicio": date(2026, 1, 1),
        "data_fim": date(2026, 1, 31),
        "situacao": SituacaoTratamento.NAO_INICIADO,
    }


@pytest.mark.django_db
def test_calcula_nivel_de_risco_e_classificacao(dados_risco):
    risco = Risco.objects.create(
        **dados_risco,
        eficacia_controles=EficaciaControle.INEXISTENTE,
    )

    assert risco.nivel_risco == 20
    assert risco.nivel_risco_display() == "Risco Extremo"


@pytest.mark.django_db
def test_calcula_nivel_residual_usando_fator_da_planilha(dados_risco):
    risco = Risco.objects.create(
        **dados_risco,
        eficacia_controles=EficaciaControle.FORTE,
    )

    assert risco.nivel_residual == 4
    assert risco.nivel_residual_display() == "Risco Moderado"


def test_classifica_niveis_conforme_faixas_da_planilha():
    assert Risco.classificar_nivel(3) == "Risco Baixo"
    assert Risco.classificar_nivel(4) == "Risco Moderado"
    assert Risco.classificar_nivel(12) == "Risco Alto"
    assert Risco.classificar_nivel(20) == "Risco Extremo"

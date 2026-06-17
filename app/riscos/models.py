import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.db import models


class TipoRisco(models.TextChoices):
    ESTRATEGICO = "ESTRATEGICO", "Estratégico"
    OPERACIONAL = "OPERACIONAL", "Operacional"
    FINANCEIRO = "FINANCEIRO", "Financeiro"
    CONFORMIDADE = "CONFORMIDADE", "Conformidade"
    IMAGEM = "IMAGEM", "Imagem"


class EscalaRisco(models.IntegerChoices):
    MUITO_BAIXO = 1, "Muito baixo"
    BAIXO = 2, "Baixo"
    MEDIO = 3, "Médio"
    ALTO = 4, "Alto"
    MUITO_ALTO = 5, "Muito alto"


class EficaciaControle(models.TextChoices):
    INEXISTENTE = "INEXISTENTE", "Inexistente"
    FRACA = "FRACA", "Fraca"
    MEDIANA = "MEDIANA", "Mediana"
    SATISFATORIA = "SATISFATORIA", "Satisfatória"
    FORTE = "FORTE", "Forte"


class RespostaRisco(models.TextChoices):
    ACEITAR = "ACEITAR", "Aceitar"
    MITIGAR = "MITIGAR", "Mitigar"
    TRANSFERIR = "TRANSFERIR", "Transferir"
    EVITAR = "EVITAR", "Evitar"


class AcaoTratamento(models.TextChoices):
    PREVENTIVA = "PREVENTIVA", "Preventiva"
    CORRETIVA = "CORRETIVA", "Corretiva"
    MONITORAMENTO = "MONITORAMENTO", "Monitoramento"
    CONTINGENCIA = "CONTINGENCIA", "Contingência"


class SituacaoTratamento(models.TextChoices):
    NAO_INICIADO = "NAO_INICIADO", "Não iniciado"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    CONCLUIDO = "CONCLUIDO", "Concluído"
    ATRASADO = "ATRASADO", "Atrasado"


class Desafio(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=180)

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Desafio"
        verbose_name_plural = "Desafios"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Objetivo(models.Model):
    desafio = models.ForeignKey(
        Desafio,
        on_delete=models.PROTECT,
        related_name="objetivos",
    )
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.TextField()

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Objetivo"
        verbose_name_plural = "Objetivos"

    def __str__(self):
        return f"{self.codigo}: {self.descricao}"


class Macroprocesso(models.Model):
    nome = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Macroprocesso"
        verbose_name_plural = "Macroprocessos"

    def __str__(self):
        return str(self.nome)


class Risco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unidade = models.ForeignKey(
        "unidades.Unidade",
        on_delete=models.PROTECT,
        related_name="riscos",
    )
    tipo_risco = models.CharField(max_length=30, choices=TipoRisco.choices)
    desafio = models.ForeignKey(
        Desafio,
        on_delete=models.PROTECT,
        related_name="riscos",
    )
    objetivo = models.ForeignKey(
        Objetivo,
        on_delete=models.PROTECT,
        related_name="riscos",
    )
    macroprocesso = models.ForeignKey(
        Macroprocesso,
        on_delete=models.PROTECT,
        related_name="riscos",
    )
    risco_identificado = models.TextField()
    probabilidade = models.PositiveSmallIntegerField(choices=EscalaRisco.choices)
    impacto = models.PositiveSmallIntegerField(choices=EscalaRisco.choices)
    nivel_risco = models.PositiveSmallIntegerField(editable=False)
    eficacia_controles = models.CharField(
        max_length=30,
        choices=EficaciaControle.choices,
    )
    nivel_residual = models.PositiveSmallIntegerField(editable=False)
    resposta = models.CharField(max_length=30, choices=RespostaRisco.choices)
    acao = models.CharField(max_length=30, choices=AcaoTratamento.choices)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    situacao = models.CharField(max_length=30, choices=SituacaoTratamento.choices)
    criado_por_nome = models.CharField(max_length=150, default="Usuário")
    criado_por_unidade = models.ForeignKey(
        "unidades.Unidade",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="riscos_criados",
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Risco"
        verbose_name_plural = "Riscos"

    def save(self, *args, **kwargs):
        if not self.criado_por_nome or self.criado_por_nome in {"Usuario", "Usuário"}:
            from .current_user import get_current_user_name

            self.criado_por_nome = get_current_user_name()
        if not self.criado_por_unidade_id:
            from .current_user import get_current_user_department

            self.criado_por_unidade = get_current_user_department()
        self.nivel_risco = int(self.probabilidade) * int(self.impacto)
        self.nivel_residual = self._calcular_nivel_residual()
        super().save(*args, **kwargs)

    def _calcular_nivel_residual(self):
        fatores = {
            EficaciaControle.INEXISTENTE: Decimal("1"),
            EficaciaControle.FRACA: Decimal("0.8"),
            EficaciaControle.MEDIANA: Decimal("0.6"),
            EficaciaControle.SATISFATORIA: Decimal("0.4"),
            EficaciaControle.FORTE: Decimal("0.2"),
        }
        fator = fatores.get(self.eficacia_controles, Decimal("1"))
        return int(
            (Decimal(self.nivel_risco) * fator).quantize(
                Decimal("1"),
                rounding=ROUND_HALF_UP,
            )
        )

    @staticmethod
    def classificar_nivel(nivel):
        if nivel < 4:
            return "Risco Baixo"
        if nivel < 12:
            return "Risco Moderado"
        if nivel < 20:
            return "Risco Alto"
        return "Risco Extremo"

    def nivel_risco_display(self):
        return self.classificar_nivel(self.nivel_risco)

    def nivel_residual_display(self):
        return self.classificar_nivel(self.nivel_residual)

    def __str__(self):
        return f"{self.unidade} - {str(self.risco_identificado)[:60]}"

    def criado_por_display(self):
        unidade = self.criado_por_unidade or "Politécnico"
        return f"{self.criado_por_nome} - {unidade}"

    def pode_ser_editado_pelo_usuario_atual(self):
        from .current_user import user_can_manage_risco

        return user_can_manage_risco(self)

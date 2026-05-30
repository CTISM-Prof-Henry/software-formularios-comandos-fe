import uuid

from django.db import models


class TipoUnidade(models.TextChoices):
    REITORIA = "REITORIA", "Reitoria"
    DIRETORIA = "DIRETORIA", "Diretoria"
    COORDENACAO = "COORDENACAO", "Coordenacao"


class Unidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sigla = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=150)
    tipo_unidade = models.CharField(max_length=30, choices=TipoUnidade.choices)
    unidade_pai = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="subunidades",
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sigla"]
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return f"{self.sigla} - {self.nome}"

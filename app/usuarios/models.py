import uuid

from django.db import models


class PerfilAcesso(models.TextChoices):
    ADMIN = "ADMIN", "Administrador"
    GESTAO_RISCOS = "GESTAO_RISCOS", "Gestão de Riscos"
    ESTUDANTE = "ESTUDANTE", "Sem acesso"

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unidade = models.ForeignKey(
        "unidades.Unidade",
        on_delete=models.PROTECT,
        related_name="usuarios",
        null=True,
        blank=True,
    )
    matricula = models.CharField(max_length=30, unique=True, null=True, blank=True)
    nome = models.CharField(max_length=150, blank=True, default="")
    email = models.EmailField(unique=True, null=True, blank=True)
    perfil_acesso = models.CharField(
        max_length=20,
        choices=PerfilAcesso.choices,
        default=PerfilAcesso.ESTUDANTE,
    )
    senha_local_definida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        if self.matricula:
            return f"{self.nome} ({self.matricula})"
        return self.nome or self.email or "Usuário"

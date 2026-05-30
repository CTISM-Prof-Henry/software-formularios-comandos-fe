import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Risco",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("setor_departamento", models.CharField(max_length=150)),
                ("tipo_risco", models.CharField(choices=[("ESTRATEGICO", "Estrategico"), ("OPERACIONAL", "Operacional"), ("FINANCEIRO", "Financeiro"), ("CONFORMIDADE", "Conformidade"), ("IMAGEM", "Imagem")], max_length=30)),
                ("risco_identificado", models.TextField()),
                ("probabilidade", models.PositiveSmallIntegerField(choices=[(1, "Muito baixo"), (2, "Baixo"), (3, "Medio"), (4, "Alto"), (5, "Muito alto")])),
                ("impacto", models.PositiveSmallIntegerField(choices=[(1, "Muito baixo"), (2, "Baixo"), (3, "Medio"), (4, "Alto"), (5, "Muito alto")])),
                ("nivel_risco", models.PositiveSmallIntegerField(editable=False)),
                ("eficacia_controles", models.CharField(choices=[("INEXISTENTE", "Inexistente"), ("FRACA", "Fraca"), ("MEDIANA", "Mediana"), ("SATISFATORIA", "Satisfatoria"), ("FORTE", "Forte")], max_length=30)),
                ("nivel_residual", models.PositiveSmallIntegerField(editable=False)),
                ("resposta", models.CharField(choices=[("ACEITAR", "Aceitar"), ("MITIGAR", "Mitigar"), ("TRANSFERIR", "Transferir"), ("EVITAR", "Evitar")], max_length=30)),
                ("acao", models.CharField(choices=[("PREVENTIVA", "Preventiva"), ("CORRETIVA", "Corretiva"), ("MONITORAMENTO", "Monitoramento"), ("CONTINGENCIA", "Contingencia")], max_length=30)),
                ("data_inicio", models.DateField()),
                ("data_fim", models.DateField()),
                ("situacao", models.CharField(choices=[("NAO_INICIADO", "Nao iniciado"), ("EM_ANDAMENTO", "Em andamento"), ("CONCLUIDO", "Concluido"), ("ATRASADO", "Atrasado")], max_length=30)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Risco",
                "verbose_name_plural": "Riscos",
                "ordering": ["-criado_em"],
            },
        ),
    ]

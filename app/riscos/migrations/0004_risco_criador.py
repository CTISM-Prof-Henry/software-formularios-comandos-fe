from django.db import migrations, models
import django.db.models.deletion


def preencher_criador(apps, schema_editor):
    Risco = apps.get_model("riscos", "Risco")
    Unidade = apps.get_model("unidades", "Unidade")
    politecnico = (
        Unidade.objects.filter(sigla__iexact="POLITECNICO").first()
        or Unidade.objects.filter(sigla__iexact="POLI").first()
        or Unidade.objects.filter(nome__icontains="Politecnico").first()
    )
    Risco.objects.filter(criado_por_nome="").update(criado_por_nome="Usuario")
    Risco.objects.filter(criado_por_unidade__isnull=True).update(
        criado_por_unidade=politecnico
    )


class Migration(migrations.Migration):
    dependencies = [
        ("riscos", "0003_desafio_objetivo_macroprocesso"),
        ("unidades", "0002_alter_unidade_tipo_unidade"),
    ]

    operations = [
        migrations.AddField(
            model_name="risco",
            name="criado_por_nome",
            field=models.CharField(default="Usuario", max_length=150),
        ),
        migrations.AddField(
            model_name="risco",
            name="criado_por_unidade",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="riscos_criados",
                to="unidades.unidade",
            ),
        ),
        migrations.RunPython(preencher_criador, migrations.RunPython.noop),
    ]

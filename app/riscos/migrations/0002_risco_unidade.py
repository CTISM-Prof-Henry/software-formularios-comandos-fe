from django.db import migrations, models
import django.db.models.deletion


def vincular_unidades(apps, schema_editor):
    Risco = apps.get_model("riscos", "Risco")
    Unidade = apps.get_model("unidades", "Unidade")

    for risco in Risco.objects.all():
        texto = (risco.setor_departamento or "").strip()
        unidade = (
            Unidade.objects.filter(sigla__iexact=texto).first()
            or Unidade.objects.filter(nome__iexact=texto).first()
            or Unidade.objects.first()
        )
        if unidade:
            risco.unidade = unidade
            risco.save(update_fields=["unidade"])


class Migration(migrations.Migration):
    dependencies = [
        ("unidades", "0002_alter_unidade_tipo_unidade"),
        ("riscos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="risco",
            name="unidade",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="riscos",
                to="unidades.unidade",
            ),
        ),
        migrations.RunPython(vincular_unidades, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="risco",
            name="unidade",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="riscos",
                to="unidades.unidade",
            ),
        ),
        migrations.RemoveField(
            model_name="risco",
            name="setor_departamento",
        ),
    ]

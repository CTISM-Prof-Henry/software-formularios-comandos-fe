from django.db import migrations


def corrigir_nome_politecnico(apps, schema_editor):
    Unidade = apps.get_model("unidades", "Unidade")
    Unidade.objects.filter(sigla="POLI", nome="Politecnico").update(nome="Politécnico")


def desfazer_nome_politecnico(apps, schema_editor):
    Unidade = apps.get_model("unidades", "Unidade")
    Unidade.objects.filter(sigla="POLI", nome="Politécnico").update(nome="Politecnico")


class Migration(migrations.Migration):
    dependencies = [
        ("unidades", "0005_alter_unidade_tipo_unidade"),
    ]

    operations = [
        migrations.RunPython(corrigir_nome_politecnico, desfazer_nome_politecnico),
    ]

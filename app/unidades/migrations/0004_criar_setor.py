from django.db import migrations


def criar_unidade(apps, schema_editor):
    Unidade = apps.get_model("unidades", "Unidade")
    Unidade.objects.get_or_create(
        sigla="POLI",
        defaults={
            "nome": "Politecnico",
            "tipo_unidade": "COORDENACAO",
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("unidades", "0003_alter_unidade_tipo_unidade"),
    ]

    operations = [
        migrations.RunPython(criar_unidade),
    ]

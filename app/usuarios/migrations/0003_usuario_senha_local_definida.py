from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0002_perfil_acesso_gestao_riscos"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="senha_local_definida",
            field=models.BooleanField(default=False),
        ),
    ]

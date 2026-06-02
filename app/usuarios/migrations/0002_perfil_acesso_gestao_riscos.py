from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="perfil_acesso",
            field=models.CharField(
                choices=[
                    ("ADMIN", "Administrador"),
                    ("GESTAO_RISCOS", "Gestão de Riscos"),
                    ("ESTUDANTE", "Sem acesso"),
                ],
                default="ESTUDANTE",
                max_length=20,
            ),
        ),
    ]

from decimal import Decimal, ROUND_HALF_UP

from django.db import migrations


def recalcular_niveis(apps, _schema_editor):
    risco_model = apps.get_model("riscos", "Risco")
    fatores = {
        "INEXISTENTE": Decimal("1"),
        "FRACA": Decimal("0.8"),
        "MEDIANA": Decimal("0.6"),
        "SATISFATORIA": Decimal("0.4"),
        "FORTE": Decimal("0.2"),
    }

    for risco in risco_model.objects.all():
        risco.nivel_risco = int(risco.probabilidade) * int(risco.impacto)
        fator = fatores.get(risco.eficacia_controles, Decimal("1"))
        risco.nivel_residual = int(
            (Decimal(risco.nivel_risco) * fator).quantize(
                Decimal("1"),
                rounding=ROUND_HALF_UP,
            )
        )
        risco.save(update_fields=["nivel_risco", "nivel_residual"])


class Migration(migrations.Migration):

    dependencies = [
        ("riscos", "0005_alter_risco_acao_alter_risco_eficacia_controles_and_more"),
    ]

    operations = [
        migrations.RunPython(recalcular_niveis, migrations.RunPython.noop),
    ]

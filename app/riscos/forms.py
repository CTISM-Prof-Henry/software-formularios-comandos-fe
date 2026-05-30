from django import forms

from .current_user import get_current_user_units
from .models import Risco


class RiscoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unidade"].queryset = get_current_user_units()

    class Meta:
        model = Risco
        fields = [
            "unidade",
            "tipo_risco",
            "desafio",
            "objetivo",
            "macroprocesso",
            "risco_identificado",
            "probabilidade",
            "impacto",
            "eficacia_controles",
            "resposta",
            "acao",
            "data_inicio",
            "data_fim",
            "situacao",
        ]
        widgets = {
            "risco_identificado": forms.Textarea(attrs={"rows": 4}),
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "unidade": "Setor/Departamento",
            "tipo_risco": "Tipo de risco",
            "desafio": "Desafio",
            "objetivo": "Objetivo",
            "macroprocesso": "Macroprocesso",
            "risco_identificado": "Risco identificado",
            "probabilidade": "Probabilidade",
            "impacto": "Impacto",
            "eficacia_controles": "Eficacia dos controles internos",
            "resposta": "Resposta",
            "acao": "Acao",
            "data_inicio": "Data inicio",
            "data_fim": "Data fim",
            "situacao": "Situacao",
        }

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        desafio = cleaned_data.get("desafio")
        objetivo = cleaned_data.get("objetivo")
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error("data_fim", "A data fim deve ser maior ou igual a data inicio.")
        if desafio and objetivo and objetivo.desafio_id != desafio.id:
            self.add_error("objetivo", "Selecione um objetivo vinculado ao desafio escolhido.")
        return cleaned_data

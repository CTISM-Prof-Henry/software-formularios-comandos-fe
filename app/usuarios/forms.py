from django import forms

from .models import Usuario


class UsuarioProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "unidade",
            "matricula",
            "nome",
            "email",
            "perfil_acesso",
        ]

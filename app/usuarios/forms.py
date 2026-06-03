from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import PerfilAcesso, Usuario


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


class AtualizarCadastroForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha local",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
    )
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
    )

    class Meta:
        model = Usuario
        fields = ["unidade", "senha", "confirmar_senha"]
        labels = {
            "unidade": "Setor/Departamento",
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error("confirmar_senha", "As senhas informadas não conferem.")
        return cleaned_data

    def save(self, commit=True, django_user=None):
        if django_user is None:
            raise ValueError("django_user is required to update the local profile.")
        usuario = super().save(commit=False)
        usuario.matricula = django_user.username
        usuario.email = django_user.email or f"{django_user.username}@ufsm.br"
        usuario.nome = django_user.get_full_name() or django_user.username
        usuario.perfil_acesso = usuario.perfil_acesso or PerfilAcesso.ESTUDANTE
        usuario.senha_local_definida = True

        if commit:
            usuario.save()
            django_user.set_password(self.cleaned_data["senha"])
            django_user.save()
        return usuario


class CadastroLocalForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha local",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
    )
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
    )

    class Meta:
        model = Usuario
        fields = ["matricula", "nome", "email", "unidade", "senha", "confirmar_senha"]
        labels = {
            "matricula": "Matricula",
            "nome": "Nome completo",
            "email": "E-mail",
            "unidade": "Setor/Departamento",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["matricula"].required = True
        self.fields["nome"].required = True
        self.fields["email"].required = True

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"].strip()
        user_model = get_user_model()
        if user_model.objects.filter(username__iexact=matricula).exists():
            raise forms.ValidationError("Ja existe uma conta cadastrada para esta matricula.")
        if Usuario.objects.filter(matricula__iexact=matricula).exists():
            raise forms.ValidationError("Ja existe uma conta cadastrada para esta matricula.")
        return matricula

    def clean_nome(self):
        return self.cleaned_data["nome"].strip()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ja existe uma conta cadastrada para este e-mail.")
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ja existe uma conta cadastrada para este e-mail.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error("confirmar_senha", "As senhas informadas nao conferem.")
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        if not commit:
            raise ValueError("CadastroLocalForm requires commit=True.")

        usuario = super().save(commit=False)
        usuario.perfil_acesso = usuario.perfil_acesso or PerfilAcesso.ESTUDANTE
        usuario.senha_local_definida = True

        matricula = self.cleaned_data["matricula"]
        nome = self.cleaned_data["nome"]
        email = self.cleaned_data["email"]
        usuario.matricula = matricula
        usuario.nome = nome
        usuario.email = email

        user_model = get_user_model()
        django_user = user_model(
            username=matricula,
            email=email,
            is_active=True,
        )

        django_user.set_password(self.cleaned_data["senha"])
        django_user.save()

        usuario.save()
        return usuario

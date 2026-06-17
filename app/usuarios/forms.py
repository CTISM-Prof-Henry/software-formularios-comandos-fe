from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from gestao_riscos.auth import sync_user_with_profile

from .models import PerfilAcesso, Usuario


class UsuarioBaseForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "unidade",
            "matricula",
            "nome",
            "email",
            "perfil_acesso",
        ]
        labels = {
            "matricula": "Matrícula",
            "perfil_acesso": "Perfil de acesso",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_matricula = (self.instance.matricula or "").strip()

    def clean_matricula(self):
        matricula = (self.cleaned_data.get("matricula") or "").strip()
        if not matricula:
            return matricula

        user_model = get_user_model()
        user_exists = user_model.objects.filter(username__iexact=matricula)
        if self._original_matricula:
            user_exists = user_exists.exclude(username__iexact=self._original_matricula)
        if user_exists.exists():
            raise forms.ValidationError("Já existe uma conta cadastrada para esta matrícula.")
        return matricula

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            return email

        user_model = get_user_model()
        user_exists = user_model.objects.filter(email__iexact=email)
        if self._original_matricula:
            user_exists = user_exists.exclude(username__iexact=self._original_matricula)
        if user_exists.exists():
            raise forms.ValidationError("Já existe uma conta cadastrada para este e-mail.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        if not commit:
            raise ValueError(f"{self.__class__.__name__} requires commit=True.")

        usuario = forms.ModelForm.save(self, commit=False)
        usuario.save()
        self.save_m2m()
        user = get_or_create_django_user_for_usuario(usuario, self._original_matricula)
        sync_user_with_profile(user, usuario=usuario)
        if not user.has_usable_password():
            user.set_unusable_password()
        user.save()
        return usuario


class UsuarioCreateForm(UsuarioBaseForm):
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

    class Meta(UsuarioBaseForm.Meta):
        fields = UsuarioBaseForm.Meta.fields + ["senha", "confirmar_senha"]

    def clean(self):
        cleaned_data = super().clean()
        validar_confirmacao_senha(self, cleaned_data)
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        if not commit:
            raise ValueError("UsuarioCreateForm requires commit=True.")

        usuario = forms.ModelForm.save(self, commit=False)
        usuario.senha_local_definida = True
        usuario.save()
        self.save_m2m()
        user = get_or_create_django_user_for_usuario(usuario, self._original_matricula)
        sync_user_with_profile(user, usuario=usuario)
        user.set_password(self.cleaned_data["senha"])
        user.save()
        return usuario


class UsuarioUpdateForm(UsuarioBaseForm):
    pass


class ResetarSenhaUsuarioForm(forms.Form):
    senha = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
    )
    confirmar_senha = forms.CharField(
        label="Confirmar nova senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
    )

    def clean(self):
        cleaned_data = super().clean()
        validar_confirmacao_senha(self, cleaned_data)
        return cleaned_data

    @transaction.atomic
    def save(self, usuario):
        user = get_or_create_django_user_for_usuario(usuario)
        sync_user_with_profile(user, usuario=usuario)
        user.set_password(self.cleaned_data["senha"])
        user.save()
        usuario.senha_local_definida = True
        usuario.save(update_fields=["senha_local_definida", "atualizado_em"])
        return usuario


def validar_confirmacao_senha(form, cleaned_data):
    senha = cleaned_data.get("senha")
    confirmar_senha = cleaned_data.get("confirmar_senha")
    if senha and confirmar_senha and senha != confirmar_senha:
        form.add_error("confirmar_senha", "As senhas informadas não conferem.")


def get_or_create_django_user_for_usuario(usuario, original_matricula=""):
    user_model = get_user_model()
    user = None
    if original_matricula:
        user = user_model.objects.filter(username__iexact=original_matricula).first()
    if user is None and usuario.matricula:
        user = user_model.objects.filter(username__iexact=usuario.matricula).first()
    if user is None:
        user = user_model(username=usuario.matricula)
    return user


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
        validar_confirmacao_senha(self, cleaned_data)
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
            "matricula": "Matrícula",
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
            raise forms.ValidationError("Já existe uma conta cadastrada para esta matrícula.")
        if Usuario.objects.filter(matricula__iexact=matricula).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada para esta matrícula.")
        return matricula

    def clean_nome(self):
        return self.cleaned_data["nome"].strip()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada para este e-mail.")
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada para este e-mail.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        validar_confirmacao_senha(self, cleaned_data)
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

from django import forms


class LoginForm(forms.Form):
    AUTH_SOURCE_CHOICES = (
        ("ufsm", "UFSM"),
        ("local", "Sistema"),
    )

    auth_source = forms.ChoiceField(
        choices=AUTH_SOURCE_CHOICES,
        initial="ufsm",
        widget=forms.RadioSelect,
    )
    matricula = forms.CharField(
        label="Matrícula",
        max_length=30,
        widget=forms.TextInput(attrs={"autocomplete": "username", "autofocus": True}),
    )
    senha = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def clean_matricula(self):
        return self.cleaned_data["matricula"].strip()

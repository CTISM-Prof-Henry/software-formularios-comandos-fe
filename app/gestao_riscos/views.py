from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from usuarios.forms import AtualizarCadastroForm, CadastroLocalForm

from .forms import LoginForm
from .permissions import can_access_risk_module
from .user_context import get_usuario_for_django_user, needs_profile_update


def index(request):
    return render(request, "dashboard.html")


def login_page(request):
    next_url = _get_safe_next_url(request)

    if request.user.is_authenticated:
        if needs_profile_update(request.user):
            return redirect("atualizar-cadastro")
        return redirect(next_url or settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_source = form.cleaned_data["auth_source"]
            matricula = form.cleaned_data["matricula"]
            senha = form.cleaned_data["senha"]

            auth_kwargs = {
                "username": matricula,
                "password": senha,
            }
            if auth_source == "ufsm":
                auth_kwargs["auth_source"] = "ufsm"

            user = authenticate(request, **auth_kwargs)
            if user is None:
                _append_login_error(form, auth_source, matricula)
            else:
                login(request, user)
                if needs_profile_update(user):
                    return redirect("atualizar-cadastro")
                return redirect(next_url or settings.LOGIN_REDIRECT_URL)
    else:
        initial = {}
        auth_source = request.GET.get("auth_source")
        matricula = (request.GET.get("matricula") or "").strip()
        if auth_source in {"ufsm", "local"}:
            initial["auth_source"] = auth_source
        if matricula:
            initial["matricula"] = matricula
        form = LoginForm(initial=initial)

    return render(
        request,
        "login.html",
        {
            "form": form,
            "next_url": next_url,
        },
    )


def local_registration(request):
    if request.user.is_authenticated:
        if needs_profile_update(request.user):
            return redirect("atualizar-cadastro")
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = CadastroLocalForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, "Conta local criada. Entre usando a opcao Sistema.")
            query = urlencode(
                {
                    "auth_source": "local",
                    "matricula": usuario.matricula,
                }
            )
            return redirect(f"{reverse('login')}?{query}")
    else:
        form = CadastroLocalForm(
            initial={"matricula": (request.GET.get("matricula") or "").strip()}
        )

    return render(request, "cadastro_local.html", {"form": form})


def app_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def healthcheck(_request):
    return JsonResponse({"status": "ok"})


def sem_permissao(request):
    if needs_profile_update(request.user):
        return redirect("atualizar-cadastro")
    if can_access_risk_module(request.user):
        return redirect("index")
    return render(request, "sem_permissao.html", status=403)


def atualizar_cadastro(request):
    usuario = get_usuario_for_django_user(request.user)
    if request.method == "POST":
        form = AtualizarCadastroForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save(django_user=request.user)
            update_session_auth_hash(request, request.user)
            messages.success(request, "Cadastro atualizado com sucesso.")
            return redirect("index")
    else:
        form = AtualizarCadastroForm(instance=usuario)

    return render(request, "atualizar_cadastro.html", {"form": form})


def _append_login_error(form, auth_source, matricula):
    if auth_source == "local":
        user_model = get_user_model()
        user = user_model.objects.filter(username__iexact=matricula).first()
        if user is None or not user.has_usable_password():
            form.add_error(
                None,
                "Conta local nao encontrada. Crie seu cadastro local ou "
                "entre com a matricula da UFSM.",
            )
            return
        form.add_error(None, "Matricula ou senha local invalidas.")
        return

    form.add_error(None, "Matricula ou senha da biblioteca invalidas.")


def _get_safe_next_url(request):
    next_url = request.POST.get("next") or request.GET.get("next") or ""
    if not next_url:
        return ""

    if url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return ""

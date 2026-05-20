from django.urls import reverse_lazy

from gestao_riscos.crud import CrudCreateView, CrudDeleteView, CrudListView, CrudUpdateView

from .forms import UsuarioProfileForm
from .models import Usuario


class UsuarioListView(CrudListView):
    model = Usuario
    page_title = "Usuarios"
    create_url_name = "usuario-create"
    update_url_name = "usuario-update"
    delete_url_name = "usuario-delete"


class UsuarioCreateView(CrudCreateView):
    model = Usuario
    form_class = UsuarioProfileForm
    success_url = reverse_lazy("usuario-list")
    page_title = "Novo Usuario"
    page_description = "Cadastre um usuario."
    cancel_url_name = "usuario-list"


class UsuarioUpdateView(CrudUpdateView):
    model = Usuario
    form_class = UsuarioProfileForm
    success_url = reverse_lazy("usuario-list")
    page_title = "Editar Usuario"
    page_description = "Atualize os dados do usuario."
    cancel_url_name = "usuario-list"


class UsuarioDeleteView(CrudDeleteView):
    model = Usuario
    success_url = reverse_lazy("usuario-list")
    page_title = "Excluir Usuario"
    page_description = "Confirme a exclusao do usuario."
    cancel_url_name = "usuario-list"

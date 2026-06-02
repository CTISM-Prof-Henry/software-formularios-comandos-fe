from django.urls import reverse_lazy

from gestao_riscos.crud import CrudCreateView, CrudDeleteView, CrudListView, CrudUpdateView
from gestao_riscos.permissions import AdminRequiredMixin

from .forms import UsuarioProfileForm
from .models import Usuario


class UsuarioListView(AdminRequiredMixin, CrudListView):
    model = Usuario
    page_title = "Usuários"
    create_url_name = "usuario-create"
    update_url_name = "usuario-update"
    delete_url_name = "usuario-delete"


class UsuarioCreateView(AdminRequiredMixin, CrudCreateView):
    model = Usuario
    form_class = UsuarioProfileForm
    success_url = reverse_lazy("usuario-list")
    page_title = "Novo Usuário"
    page_description = "Cadastre um usuário."
    cancel_url_name = "usuario-list"


class UsuarioUpdateView(AdminRequiredMixin, CrudUpdateView):
    model = Usuario
    form_class = UsuarioProfileForm
    success_url = reverse_lazy("usuario-list")
    page_title = "Editar Usuário"
    page_description = "Atualize os dados do usuário."
    cancel_url_name = "usuario-list"


class UsuarioDeleteView(AdminRequiredMixin, CrudDeleteView):
    model = Usuario
    success_url = reverse_lazy("usuario-list")
    page_title = "Excluir Usuário"
    page_description = "Confirme a exclusão do usuário."
    cancel_url_name = "usuario-list"

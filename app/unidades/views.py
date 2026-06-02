from django.urls import reverse_lazy

from gestao_riscos.crud import CrudCreateView, CrudDeleteView, CrudListView, CrudUpdateView
from gestao_riscos.permissions import AdminRequiredMixin

from .forms import UnidadeForm
from .models import Unidade


class UnidadeListView(AdminRequiredMixin, CrudListView):
    model = Unidade
    page_title = "Unidades"
    create_url_name = "unidade-create"
    update_url_name = "unidade-update"
    delete_url_name = "unidade-delete"


class UnidadeCreateView(AdminRequiredMixin, CrudCreateView):
    model = Unidade
    form_class = UnidadeForm
    success_url = reverse_lazy("unidade-list")
    page_title = "Nova Unidade"
    page_description = "Cadastre uma unidade ou setor."
    cancel_url_name = "unidade-list"


class UnidadeUpdateView(AdminRequiredMixin, CrudUpdateView):
    model = Unidade
    form_class = UnidadeForm
    success_url = reverse_lazy("unidade-list")
    page_title = "Editar Unidade"
    page_description = "Atualize os dados da unidade selecionada."
    cancel_url_name = "unidade-list"


class UnidadeDeleteView(AdminRequiredMixin, CrudDeleteView):
    model = Unidade
    success_url = reverse_lazy("unidade-list")
    page_title = "Excluir Unidade"
    page_description = "Confirme a exclusão da unidade."
    cancel_url_name = "unidade-list"

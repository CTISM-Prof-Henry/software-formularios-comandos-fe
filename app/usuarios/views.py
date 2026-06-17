from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from gestao_riscos.crud import CrudCreateView, CrudDeleteView, CrudListView, CrudUpdateView
from gestao_riscos.permissions import AdminRequiredMixin

from .forms import ResetarSenhaUsuarioForm, UsuarioCreateForm, UsuarioUpdateForm
from .models import Usuario


class UsuarioListView(AdminRequiredMixin, CrudListView):
    model = Usuario
    page_title = "Usuários"
    create_url_name = "usuario-create"
    update_url_name = "usuario-update"
    delete_url_name = "usuario-delete"


class UsuarioCreateView(AdminRequiredMixin, CrudCreateView):
    model = Usuario
    form_class = UsuarioCreateForm
    success_url = reverse_lazy("usuario-list")
    page_title = "Novo Usuário"
    page_description = "Cadastre um usuário."
    cancel_url_name = "usuario-list"


class UsuarioUpdateView(AdminRequiredMixin, CrudUpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm
    success_url = reverse_lazy("usuario-list")
    page_title = "Editar Usuário"
    page_description = "Atualize os dados do usuário."
    cancel_url_name = "usuario-list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_form_action_url"] = reverse(
            "usuario-reset-password",
            kwargs={"pk": self.object.pk},
        )
        context["extra_form_action_label"] = "Resetar senha"
        context["extra_form_action_icon"] = "fa-key"
        return context


class UsuarioResetPasswordView(AdminRequiredMixin, FormView):
    template_name = "crud/form.html"
    form_class = ResetarSenhaUsuarioForm
    success_url = reverse_lazy("usuario-list")
    page_title = "Resetar Senha"
    page_description = "Defina uma nova senha local para o usuário."
    cancel_url_name = "usuario-list"
    submit_label = "Salvar nova senha"

    def dispatch(self, request, *args, **kwargs):
        self.object = Usuario.objects.get(pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["page_description"] = self.page_description
        context["cancel_url"] = reverse("usuario-update", kwargs={"pk": self.object.pk})
        context["submit_label"] = self.submit_label
        return context

    def form_valid(self, form):
        form.save(self.object)
        return super().form_valid(form)


class UsuarioDeleteView(AdminRequiredMixin, CrudDeleteView):
    model = Usuario
    success_url = reverse_lazy("usuario-list")
    page_title = "Excluir Usuário"
    page_description = "Confirme a exclusão do usuário."
    cancel_url_name = "usuario-list"

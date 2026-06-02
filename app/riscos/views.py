from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import DetailView

from gestao_riscos.crud import CrudCreateView, CrudDeleteView, CrudListView, CrudUpdateView
from gestao_riscos.permissions import RiskModuleRequiredMixin, is_admin

from .forms import RiscoForm
from .current_user import (
    get_current_user_department,
    get_current_user_name,
    get_current_user_units,
    user_can_manage_risco,
)
from .models import Objetivo, Risco


class RiscoListView(RiskModuleRequiredMixin, CrudListView):
    model = Risco
    template_name = "riscos/list.html"
    page_title = "Análise de Riscos"
    create_url_name = "risco-create"
    update_url_name = "risco-update"
    delete_url_name = "risco-delete"
    create_label = "Novo Plano"

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_admin(self.request.user):
            return queryset
        return queryset.filter(unidade__in=get_current_user_units()).distinct()


class RiscoFormContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objetivos_por_desafio"] = [
            {
                "id": str(objetivo.id),
                "desafio_id": str(objetivo.desafio_id),
                "label": str(objetivo),
            }
            for objetivo in Objetivo.objects.select_related("desafio")
        ]
        return context


class RiscoCreateView(RiskModuleRequiredMixin, RiscoFormContextMixin, CrudCreateView):
    model = Risco
    form_class = RiscoForm
    template_name = "riscos/form.html"
    success_url = reverse_lazy("risco-list")
    page_title = "Análise de Riscos"
    page_description = "Preencha todos os campos para uma análise completa."
    cancel_url_name = "risco-list"
    submit_label = "Salvar Novo Plano"

    def form_valid(self, form):
        form.instance.criado_por_nome = get_current_user_name()
        form.instance.criado_por_unidade = get_current_user_department()
        return super().form_valid(form)


class RiscoUpdateView(RiskModuleRequiredMixin, RiscoFormContextMixin, CrudUpdateView):
    model = Risco
    form_class = RiscoForm
    template_name = "riscos/form.html"
    success_url = reverse_lazy("risco-list")
    page_title = "Editar Análise de Riscos"
    page_description = "Atualize a identificação, avaliação e tratamento do risco."
    cancel_url_name = "risco-list"
    submit_label = "Salvar Alteracoes"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not user_can_manage_risco(self.object):
            return HttpResponseForbidden("Você não pode editar riscos desta unidade.")
        return super().dispatch(request, *args, **kwargs)


class RiscoDeleteView(RiskModuleRequiredMixin, CrudDeleteView):
    model = Risco
    success_url = reverse_lazy("risco-list")
    page_title = "Excluir Análise de Riscos"
    page_description = "Confirme a exclusão da análise selecionada."
    cancel_url_name = "risco-list"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not user_can_manage_risco(self.object):
            return HttpResponseForbidden("Você não pode excluir riscos desta unidade.")
        return super().dispatch(request, *args, **kwargs)


class RiscoPrintView(RiskModuleRequiredMixin, DetailView):
    model = Risco
    template_name = "riscos/print.html"
    context_object_name = "risco"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not user_can_manage_risco(self.object):
            return HttpResponseForbidden("Você não pode visualizar riscos de outro usuário.")
        return super().dispatch(request, *args, **kwargs)

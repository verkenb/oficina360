from django.urls import path

from . import views

app_name = "estoque"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pecas/", views.lista_pecas, name="pecas_lista"),
    path("pecas/nova/", views.nova_peca, name="peca_nova"),
    path("pecas/<int:pk>/editar/", views.editar_peca, name="peca_editar"),
    path("fornecedores/", views.lista_fornecedores, name="fornecedores_lista"),
    path("fornecedores/novo/", views.novo_fornecedor, name="fornecedor_novo"),
    path("movimentacoes/", views.lista_movimentacoes, name="movimentacoes_lista"),
    path("movimentacoes/nova/", views.nova_movimentacao, name="movimentacao_nova"),
]

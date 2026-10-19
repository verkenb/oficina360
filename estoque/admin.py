from django.contrib import admin

from .models import Fornecedor, Movimentacao, Peca


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email")
    search_fields = ("nome", "email")


@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "quantidade", "estoque_minimo", "preco_custo", "fornecedor")
    list_filter = ("categoria", "unidade")
    search_fields = ("codigo", "nome", "categoria")
    readonly_fields = ("quantidade", "criado_em", "atualizado_em")
    fields = ("codigo", "nome", "categoria", "unidade", "estoque_minimo", "preco_custo", "fornecedor", "descricao", "quantidade", "criado_em", "atualizado_em")


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("criado_em", "peca", "tipo", "quantidade", "observacao")
    list_filter = ("tipo", "criado_em")
    search_fields = ("peca__nome", "peca__codigo", "observacao")
    readonly_fields = ("peca", "tipo", "quantidade", "observacao", "criado_em")

    def has_add_permission(self, request):
        # Movimentações devem ser criadas pela aplicação para atualizar o saldo corretamente.
        return False

    def has_change_permission(self, request, obj=None):
        return False

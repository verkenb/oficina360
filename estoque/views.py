from decimal import Decimal

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FornecedorForm, MovimentacaoForm, PecaForm
from .models import Fornecedor, Movimentacao, Peca
from .services import registrar_movimentacao


def dashboard(request):
    pecas = Peca.objects.all()
    movimentos_recentes = Movimentacao.objects.select_related("peca")[:8]
    valor_estoque = sum((peca.valor_total_estoque for peca in pecas), Decimal("0.00"))
    pecas_baixo_estoque = Peca.objects.filter(quantidade__lte=F("estoque_minimo"))
    context = {
        "total_pecas": pecas.count(),
        "baixo_estoque": pecas_baixo_estoque.count(),
        "total_fornecedores": Fornecedor.objects.count(),
        "total_movimentacoes": Movimentacao.objects.count(),
        "valor_estoque": valor_estoque,
        "movimentos_recentes": movimentos_recentes,
        "pecas_baixo_estoque": pecas_baixo_estoque.select_related("fornecedor")[:6],
    }
    return render(request, "estoque/dashboard.html", context)


def lista_pecas(request):
    termo = request.GET.get("q", "").strip()
    apenas_baixo_estoque = request.GET.get("baixo") == "1"
    pecas = Peca.objects.select_related("fornecedor")
    if termo:
        pecas = pecas.filter(
            Q(codigo__icontains=termo)
            | Q(nome__icontains=termo)
            | Q(categoria__icontains=termo)
            | Q(fornecedor__nome__icontains=termo)
        )
    if apenas_baixo_estoque:
        pecas = pecas.filter(quantidade__lte=F("estoque_minimo"))
    return render(request, "estoque/pecas_lista.html", {
        "pecas": pecas,
        "termo": termo,
        "apenas_baixo_estoque": apenas_baixo_estoque,
    })


def nova_peca(request):
    if request.method == "POST":
        form = PecaForm(request.POST)
        if form.is_valid():
            peca = form.save()
            messages.success(request, f"Peça '{peca.nome}' cadastrada. Registre uma entrada para adicionar saldo ao estoque.")
            return redirect("estoque:pecas_lista")
    else:
        form = PecaForm()
    return render(request, "estoque/peca_form.html", {"form": form, "titulo": "Cadastrar peça"})


def editar_peca(request, pk):
    peca = get_object_or_404(Peca, pk=pk)
    if request.method == "POST":
        form = PecaForm(request.POST, instance=peca)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro da peça atualizado.")
            return redirect("estoque:pecas_lista")
    else:
        form = PecaForm(instance=peca)
    return render(request, "estoque/peca_form.html", {"form": form, "titulo": "Editar peça", "peca": peca})


def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, "estoque/fornecedores_lista.html", {"fornecedores": fornecedores})


def novo_fornecedor(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f"Fornecedor '{fornecedor.nome}' cadastrado.")
            return redirect("estoque:fornecedores_lista")
    else:
        form = FornecedorForm()
    return render(request, "estoque/fornecedor_form.html", {"form": form, "titulo": "Cadastrar fornecedor"})


def lista_movimentacoes(request):
    movimentos = Movimentacao.objects.select_related("peca")
    return render(request, "estoque/movimentacoes_lista.html", {"movimentos": movimentos[:100]})


def nova_movimentacao(request):
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            try:
                registrar_movimentacao(
                    peca_id=dados["peca"].pk,
                    tipo=dados["tipo"],
                    quantidade=dados["quantidade"],
                    observacao=dados["observacao"],
                )
            except ValidationError as erro:
                form.add_error(None, erro)
            else:
                tipo_texto = "Entrada" if dados["tipo"] == Movimentacao.Tipo.ENTRADA else "Saída"
                messages.success(request, f"{tipo_texto} registrada para '{dados['peca'].nome}'.")
                return redirect("estoque:movimentacoes_lista")
    else:
        initial = {}
        peca_id = request.GET.get("peca")
        if peca_id and peca_id.isdigit() and Peca.objects.filter(pk=int(peca_id)).exists():
            initial["peca"] = int(peca_id)
        form = MovimentacaoForm(initial=initial)
    return render(request, "estoque/movimentacao_form.html", {"form": form, "titulo": "Nova movimentação"})

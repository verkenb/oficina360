from django import forms

from .models import Fornecedor, Peca, Movimentacao


class EstilizaFormularioMixin:
    """Adiciona classes CSS aos campos para manter os formulários consistentes."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            current = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{current} form-control".strip()


class FornecedorForm(EstilizaFormularioMixin, forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ["nome", "telefone", "email"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Auto Peças Central"}),
            "telefone": forms.TextInput(attrs={"placeholder": "(00) 00000-0000"}),
            "email": forms.EmailInput(attrs={"placeholder": "fornecedor@exemplo.com"}),
        }


class PecaForm(EstilizaFormularioMixin, forms.ModelForm):
    class Meta:
        model = Peca
        fields = [
            "codigo", "nome", "categoria", "unidade", "estoque_minimo",
            "preco_custo", "fornecedor", "descricao",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"placeholder": "Ex.: OLEO-10W40"}),
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Óleo de motor 10W-40"}),
            "categoria": forms.TextInput(attrs={"placeholder": "Ex.: Lubrificantes"}),
            "estoque_minimo": forms.NumberInput(attrs={"min": 0}),
            "preco_custo": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "descricao": forms.Textarea(attrs={"rows": 3, "placeholder": "Detalhes opcionais sobre a peça"}),
        }
        help_texts = {
            "estoque_minimo": "Quando a quantidade ficar igual ou abaixo deste valor, o sistema sinaliza estoque baixo.",
            "preco_custo": "Informe o custo de uma unidade, não o valor total do estoque.",
        }


class MovimentacaoForm(EstilizaFormularioMixin, forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ["peca", "tipo", "quantidade", "observacao"]
        widgets = {
            "quantidade": forms.NumberInput(attrs={"min": 1, "step": 1}),
            "observacao": forms.TextInput(attrs={"placeholder": "Ex.: compra de fornecedor, troca de óleo..."}),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade < 1:
            raise forms.ValidationError("Informe uma quantidade maior que zero.")
        return quantidade

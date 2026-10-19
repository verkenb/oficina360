from django.core.validators import MinValueValidator
from django.db import models


class Fornecedor(models.Model):
    nome = models.CharField("Nome do fornecedor", max_length=120)
    telefone = models.CharField("Telefone", max_length=30, blank=True)
    email = models.EmailField("E-mail", blank=True)
    criado_em = models.DateTimeField("Cadastrado em", auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "fornecedor"
        verbose_name_plural = "fornecedores"

    def __str__(self):
        return self.nome


class Peca(models.Model):
    class Unidade(models.TextChoices):
        UNIDADE = "un", "Unidade"
        JOGO = "jogo", "Jogo"
        PAR = "par", "Par"

    codigo = models.CharField("Código/SKU", max_length=40, unique=True)
    nome = models.CharField("Nome da peça", max_length=140)
    categoria = models.CharField("Categoria", max_length=80, blank=True)
    unidade = models.CharField("Unidade", max_length=8, choices=Unidade.choices, default=Unidade.UNIDADE)
    quantidade = models.PositiveIntegerField("Quantidade em estoque", default=0)
    estoque_minimo = models.PositiveIntegerField("Estoque mínimo", default=1)
    preco_custo = models.DecimalField(
        "Custo unitário (R$)", max_digits=10, decimal_places=2,
        default=0, validators=[MinValueValidator(0)],
    )
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="pecas", verbose_name="Fornecedor principal",
    )
    descricao = models.TextField("Observações", blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "peça"
        verbose_name_plural = "peças"

    def __str__(self):
        return f"{self.codigo} — {self.nome}"

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo

    @property
    def valor_total_estoque(self):
        return self.quantidade * self.preco_custo


class Movimentacao(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "entrada", "Entrada"
        SAIDA = "saida", "Saída"

    peca = models.ForeignKey(
        Peca, on_delete=models.PROTECT, related_name="movimentacoes", verbose_name="Peça",
    )
    tipo = models.CharField("Tipo", max_length=10, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField("Quantidade", validators=[MinValueValidator(1)])
    observacao = models.CharField("Observação", max_length=250, blank=True)
    criado_em = models.DateTimeField("Data e hora", auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "movimentação"
        verbose_name_plural = "movimentações"

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.peca.nome} ({self.quantidade})"

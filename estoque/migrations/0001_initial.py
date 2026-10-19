# Generated for Oficina360. Do not edit unless you know how Django migrations work.
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Fornecedor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120, verbose_name="Nome do fornecedor")),
                ("telefone", models.CharField(blank=True, max_length=30, verbose_name="Telefone")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="E-mail")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="Cadastrado em")),
            ],
            options={"verbose_name": "fornecedor", "verbose_name_plural": "fornecedores", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="Peca",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=40, unique=True, verbose_name="Código/SKU")),
                ("nome", models.CharField(max_length=140, verbose_name="Nome da peça")),
                ("categoria", models.CharField(blank=True, max_length=80, verbose_name="Categoria")),
                ("unidade", models.CharField(choices=[("un", "Unidade"), ("jogo", "Jogo"), ("par", "Par")], default="un", max_length=8, verbose_name="Unidade")),
                ("quantidade", models.PositiveIntegerField(default=0, verbose_name="Quantidade em estoque")),
                ("estoque_minimo", models.PositiveIntegerField(default=1, verbose_name="Estoque mínimo")),
                ("preco_custo", models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Custo unitário (R$)")),
                ("descricao", models.TextField(blank=True, verbose_name="Observações")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="Criado em")),
                ("atualizado_em", models.DateTimeField(auto_now=True, verbose_name="Atualizado em")),
                ("fornecedor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="pecas", to="estoque.fornecedor", verbose_name="Fornecedor principal")),
            ],
            options={"verbose_name": "peça", "verbose_name_plural": "peças", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="Movimentacao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("entrada", "Entrada"), ("saida", "Saída")], max_length=10, verbose_name="Tipo")),
                ("quantidade", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name="Quantidade")),
                ("observacao", models.CharField(blank=True, max_length=250, verbose_name="Observação")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="Data e hora")),
                ("peca", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="movimentacoes", to="estoque.peca", verbose_name="Peça")),
            ],
            options={"verbose_name": "movimentação", "verbose_name_plural": "movimentações", "ordering": ["-criado_em"]},
        ),
    ]

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Fornecedor, Movimentacao, Peca
from .services import registrar_movimentacao


class MovimentacaoServiceTests(TestCase):
    def setUp(self):
        self.peca = Peca.objects.create(
            codigo="OLEO-001",
            nome="Óleo 10W-40",
            quantidade=5,
            estoque_minimo=2,
            preco_custo="35.90",
        )

    def test_entrada_aumenta_saldo_e_cria_historico(self):
        movimento = registrar_movimentacao(
            peca_id=self.peca.pk,
            tipo=Movimentacao.Tipo.ENTRADA,
            quantidade=3,
            observacao="Compra de teste",
        )
        self.peca.refresh_from_db()
        self.assertEqual(self.peca.quantidade, 8)
        self.assertEqual(movimento.tipo, Movimentacao.Tipo.ENTRADA)
        self.assertEqual(Movimentacao.objects.count(), 1)

    def test_saida_reduz_saldo(self):
        registrar_movimentacao(
            peca_id=self.peca.pk,
            tipo=Movimentacao.Tipo.SAIDA,
            quantidade=2,
        )
        self.peca.refresh_from_db()
        self.assertEqual(self.peca.quantidade, 3)

    def test_saida_acima_do_saldo_e_rejeitada(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao(
                peca_id=self.peca.pk,
                tipo=Movimentacao.Tipo.SAIDA,
                quantidade=6,
            )
        self.peca.refresh_from_db()
        self.assertEqual(self.peca.quantidade, 5)
        self.assertEqual(Movimentacao.objects.count(), 0)

    def test_quantidade_zero_e_rejeitada(self):
        with self.assertRaises(ValidationError):
            registrar_movimentacao(
                peca_id=self.peca.pk,
                tipo=Movimentacao.Tipo.ENTRADA,
                quantidade=0,
            )


class PaginasPrincipaisTests(TestCase):
    def test_dashboard_abre(self):
        resposta = self.client.get(reverse("estoque:dashboard"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Visão geral")

    def test_lista_de_pecas_abre(self):
        resposta = self.client.get(reverse("estoque:pecas_lista"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Peças e estoque")

    def test_fornecedor_pode_ser_cadastrado(self):
        resposta = self.client.post(reverse("estoque:fornecedor_novo"), {
            "nome": "Auto Peças Exemplo",
            "telefone": "31999990000",
            "email": "contato@example.com",
        })
        self.assertRedirects(resposta, reverse("estoque:fornecedores_lista"))
        self.assertTrue(Fornecedor.objects.filter(nome="Auto Peças Exemplo").exists())

"""Regras de negócio para movimentar o estoque com segurança."""
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Movimentacao, Peca


@transaction.atomic
def registrar_movimentacao(*, peca_id, tipo, quantidade, observacao=""):
    """Registra entrada/saída e atualiza o saldo dentro de uma transação.

    Essa função deve ser usada em vez de criar Movimentacao diretamente, pois mantém
    o saldo da peça sincronizado com o histórico de movimentações.
    """
    if tipo not in Movimentacao.Tipo.values:
        raise ValidationError("Selecione um tipo de movimentação válido.")
    if not isinstance(quantidade, int) or quantidade < 1:
        raise ValidationError("A quantidade precisa ser um número inteiro maior que zero.")

    try:
        peca = Peca.objects.select_for_update().get(pk=peca_id)
    except Peca.DoesNotExist as exc:
        raise ValidationError("A peça selecionada não existe.") from exc

    if tipo == Movimentacao.Tipo.SAIDA and quantidade > peca.quantidade:
        raise ValidationError(
            f"Estoque insuficiente: há {peca.quantidade} unidade(s) de '{peca.nome}'."
        )

    if tipo == Movimentacao.Tipo.ENTRADA:
        peca.quantidade += quantidade
    else:
        peca.quantidade -= quantidade

    peca.save(update_fields=["quantidade", "atualizado_em"])
    return Movimentacao.objects.create(
        peca=peca,
        tipo=tipo,
        quantidade=quantidade,
        observacao=observacao.strip(),
    )

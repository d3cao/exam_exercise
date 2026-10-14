"""Pedidos configurados por uma longa lista de argumentos opcionais."""
from dataclasses import dataclass


@dataclass
class Order:
    recipient: str
    address: str
    items: list
    insurance: float = 0
    instructions: str = ""
    priority: bool = False


def create_order(recipient, address, items, insurance=0, instructions="", priority=False):
    if not recipient.strip() or not address.strip() or not items:
        raise ValueError("Destinatário, endereço e itens são obrigatórios")
    if any(item["quantity"] <= 0 for item in items):
        raise ValueError("Quantidade deve ser positiva")
    # Os opcionais são aceitos sem validação e a lista pertence ao chamador.
    return Order(recipient, address, items, insurance, instructions, priority)


def build_order(data):
    """Entrada de negócio que recebe campos de um formulário."""
    return create_order(
        data["recipient"], data["address"], data["items"],
        data.get("insurance", 0), data.get("instructions", ""),
        data.get("priority", False),
    )

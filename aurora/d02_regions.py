"""Documentos e tarifas escolhidos separadamente pela operação."""


def label(country, order_id):
    if country == "BR":
        return {"country": "BR", "text": f"Entrega {order_id}"}
    raise ValueError("País desconhecido")


def receipt(country, order_id):
    if country == "BR":
        return {"country": "BR", "text": f"Comprovante {order_id}"}
    raise ValueError("País desconhecido")


def freight(country, weight):
    if weight <= 0:
        raise ValueError("Peso deve ser positivo")
    if country == "BR":
        return {"country": "BR", "currency": "BRL", "amount": 10 + 2 * weight}
    raise ValueError("País desconhecido")


def prepare(country, order_id, weight):
    # A região de cada produto é escolhida manualmente em cada fluxo.
    return {
        "label": label(country, order_id),
        "receipt": receipt("BR", order_id),
        "freight": freight("BR", weight),
    }

"""Tipos de documento e canais misturados nas classes existentes."""
from html import escape


class LabelText:
    def render(self, order):
        return f"Etiqueta: {order['id']} - {order['recipient']}"


class LabelHtml:
    def render(self, order):
        return f"<p>Etiqueta: {escape(order['id'])} - {escape(order['recipient'])}</p>"


class ReceiptText:
    def render(self, order):
        return f"Comprovante: {order['id']} - {order['recipient']}"


def render(kind, channel, order):
    if kind == "label" and channel == "text":
        return LabelText().render(order)
    if kind == "label" and channel == "html":
        return LabelHtml().render(order)
    if kind == "receipt" and channel == "text":
        return ReceiptText().render(order)
    raise ValueError("Combinação de documento e canal indisponível")

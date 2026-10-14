"""Dois fornecedores com contratos de transporte incompatíveis."""
from xml.sax.saxutils import escape


class ModernCarrier:
    def send(self, payload):
        if payload["weight"] <= 0:
            raise ValueError("Peso deve ser positivo")
        return {"tracking": f"MOD-{payload['order_id']}", "status": "accepted"}


class LegacyCarrier:
    def __init__(self):
        self.requests = []

    def submit(self, record):
        self.requests.append(record)
        order_id, weight, postal_code = record.split("|")
        if float(weight) <= 0:
            raise ValueError("Peso deve ser positivo")
        return f"<shipment><tracking>LEG-{escape(order_id)}</tracking><status>accepted</status></shipment>"


def ship(payload, carrier):
    return carrier.send(payload)

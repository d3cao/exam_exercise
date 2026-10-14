"""Pedidos recorrentes baseados em modelos de campanha."""
from copy import copy


class Campaigns:
    def __init__(self):
        self.templates = {
            "welcome": {
                "recipient": "Cliente", "address": {"city": "Recife", "street": "Rua A"},
                "items": [{"sku": "KIT", "quantity": 1}],
            }
        }

    def save(self, name, order):
        self.templates[name] = order

    def spawn(self, name):
        return copy(self.templates[name])

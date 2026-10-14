"""Cada serviço carrega sua própria configuração operacional."""


class Settings:
    loads = 0

    def __init__(self):
        Settings.loads += 1
        self.currency = "BRL"
        self.max_weight = 30

    def update(self, *, currency=None, max_weight=None):
        if max_weight is not None and max_weight <= 0:
            raise ValueError("Limite deve ser positivo")
        if currency is not None:
            self.currency = currency
        if max_weight is not None:
            self.max_weight = max_weight


def get_settings():
    return Settings()


class QuoteService:
    def __init__(self):
        self.settings = get_settings()


class DispatchService:
    def __init__(self):
        self.settings = get_settings()

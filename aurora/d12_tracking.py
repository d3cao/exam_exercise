"""Consulta direta a um fornecedor caro de inicializar."""


class Provider:
    def __init__(self):
        self.calls = []
        self.fail_next = False

    def fetch(self, code):
        self.calls.append(code)
        if self.fail_next:
            self.fail_next = False
            raise ConnectionError("Fornecedor temporariamente indisponível")
        return {"code": code, "status": "in_transit"}


class ProviderLoader:
    def __init__(self):
        self.loads = 0
        self.instance = None

    def __call__(self):
        self.loads += 1
        self.instance = Provider()
        return self.instance


class Tracking:
    def __init__(self, loader):
        self.provider = loader()

    def lookup(self, code, authorized=True):
        return self.provider.fetch(code)

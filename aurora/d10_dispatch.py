"""Cliente responsável por conhecer todas as etapas do despacho."""


class Operations:
    def __init__(self, fail_at=None):
        self.events = []
        self.fail_at = fail_at

    def _record(self, step, order_id):
        self.events.append((step, order_id))
        if step == self.fail_at:
            raise RuntimeError(f"Falha em {step}")

    def reserve(self, order_id):
        self._record("stock", order_id)

    def charge(self, order_id):
        self._record("payment", order_id)

    def label(self, order_id):
        self._record("label", order_id)
        return f"LABEL-{order_id}"

    def collect(self, order_id):
        self._record("collection", order_id)
        return f"PICKUP-{order_id}"


def manual_dispatch(order_id, operations):
    operations.reserve(order_id)
    operations.charge(order_id)
    label = operations.label(order_id)
    pickup = operations.collect(order_id)
    return {"label": label, "pickup": pickup}


def dispatch(order_id, operations):
    """Entrada reservada para o novo fluxo coordenado."""
    raise NotImplementedError("Fluxo ainda usado manualmente pelos clientes")

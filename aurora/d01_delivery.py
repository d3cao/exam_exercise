"""Cotação, despacho e rastreamento das modalidades existentes."""


class RoadDelivery:
    def quote(self, weight):
        return 10 + weight * 2

    def dispatch(self, order_id):
        return f"ROAD-{order_id}"

    def track(self, code):
        return {"code": code, "vehicle": "truck"}


class AirDelivery:
    def quote(self, weight):
        return 30 + weight * 5

    def dispatch(self, order_id):
        return f"AIR-{order_id}"

    def track(self, code):
        return {"code": code, "vehicle": "plane"}


def quote(mode, weight):
    if weight <= 0:
        raise ValueError("Peso deve ser positivo")
    if mode == "road":
        delivery = RoadDelivery()
    elif mode == "air":
        delivery = AirDelivery()
    else:
        raise ValueError("Modalidade desconhecida")
    return delivery.quote(weight)


def dispatch(mode, order_id):
    if mode == "road":
        delivery = RoadDelivery()
    elif mode == "air":
        delivery = AirDelivery()
    else:
        raise ValueError("Modalidade desconhecida")
    return delivery.dispatch(order_id)


def track(mode, code):
    if mode == "road":
        delivery = RoadDelivery()
    elif mode == "air":
        delivery = AirDelivery()
    else:
        raise ValueError("Modalidade desconhecida")
    return delivery.track(code)

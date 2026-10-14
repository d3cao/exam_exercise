"""Somatórios escritos para cada formato conhecido de carga."""


def totals(cargo):
    if cargo["kind"] == "item":
        if cargo["weight"] < 0 or cargo["price"] < 0:
            raise ValueError("Peso e preço não podem ser negativos")
        return {"weight": cargo["weight"], "price": cargo["price"]}
    if cargo["kind"] == "box":
        weight = price = 0
        for item in cargo["children"]:
            # Caixas existentes só contêm itens individuais.
            weight += item["weight"]
            price += item["price"]
        return {"weight": weight, "price": price}
    raise ValueError("Tipo de carga desconhecido")

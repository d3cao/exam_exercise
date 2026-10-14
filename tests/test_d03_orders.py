import pytest
from aurora import d03_orders as api


def form():
    return {"recipient": "Ana", "address": "Rua A", "items": [{"sku": "KIT", "quantity": 1}]}


def test_basic_order():
    order = api.build_order(form())
    assert (order.recipient, order.address, order.insurance, order.instructions, order.priority) == ("Ana", "Rua A", 0, "", False)
    assert order.items == [{"sku": "KIT", "quantity": 1}]


def test_optional_fields_and_compatible_entrypoint():
    data = form()
    data.update(insurance=100, instructions="Portaria", priority=True)
    order = api.build_order(data)
    compatible = api.create_order("Ana", "Rua A", data["items"], 100, "Portaria", True)
    assert order == compatible
    assert (order.insurance, order.instructions, order.priority) == (100, "Portaria", True)


@pytest.mark.parametrize("field,value", [("recipient", " "), ("address", ""), ("items", []), ("items", [{"sku": "KIT", "quantity": 0}])])
def test_required_validation(field, value):
    data = form()
    data[field] = value
    with pytest.raises(ValueError):
        api.build_order(data)


@pytest.mark.xfail(strict=True, reason="Isolamento de montagem pendente")
def test_orders_own_nested_items():
    data = form()
    data.update(insurance=100, instructions="Portaria", priority=True)
    first = api.build_order(data)
    second = api.build_order(data)
    data["items"][0]["quantity"] = 9
    assert first.items[0]["quantity"] == second.items[0]["quantity"] == 1
    first.items[0]["quantity"] = 3
    assert second.items[0]["quantity"] == 1
    assert (first.insurance, first.instructions, first.priority) == (100, "Portaria", True)


@pytest.mark.xfail(strict=True, reason="Validação dos opcionais pendente")
@pytest.mark.parametrize("value", [-1, -100])
def test_negative_insurance(value):
    data = form()
    data["insurance"] = value
    with pytest.raises(ValueError):
        api.build_order(data)

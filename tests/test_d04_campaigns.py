import pytest
from aurora.d04_campaigns import Campaigns


def test_default_template():
    order = Campaigns().spawn("welcome")
    assert order["items"] == [{"sku": "KIT", "quantity": 1}]
    assert order["address"]["city"] == "Recife"


def test_missing_template():
    with pytest.raises(KeyError):
        Campaigns().spawn("missing")


@pytest.mark.xfail(strict=True, reason="Pedidos derivados independentes pendentes")
def test_nested_changes_do_not_change_template_or_sibling():
    campaigns = Campaigns()
    first, second = campaigns.spawn("welcome"), campaigns.spawn("welcome")
    first["items"][0]["quantity"] = 8
    first["address"]["city"] = "Natal"
    assert second["items"][0]["quantity"] == 1
    assert second["address"]["city"] == "Recife"
    assert campaigns.spawn("welcome") == second


@pytest.mark.xfail(strict=True, reason="Armazenamento independente do modelo pendente")
def test_saved_template_owns_input():
    campaigns = Campaigns()
    data = {"address": {"city": "Olinda"}, "items": [{"sku": "BOOK", "quantity": 2}], "note": "Especial"}
    campaigns.save("books", data)
    data["items"][0]["quantity"] = 99
    data["address"]["city"] = "Natal"
    result = campaigns.spawn("books")
    assert result == {"address": {"city": "Olinda"}, "items": [{"sku": "BOOK", "quantity": 2}], "note": "Especial"}

import pytest
from aurora import d02_regions as api


def test_brazil_bundle():
    assert api.prepare("BR", "42", 2) == {
        "label": {"country": "BR", "text": "Entrega 42"},
        "receipt": {"country": "BR", "text": "Comprovante 42"},
        "freight": {"country": "BR", "currency": "BRL", "amount": 14},
    }


@pytest.mark.parametrize("country,weight", [("ZZ", 1), ("BR", 0), ("BR", -2)])
def test_invalid_request(country, weight):
    with pytest.raises(ValueError):
        api.prepare(country, "42", weight)


@pytest.mark.xfail(strict=True, reason="Operação regional completa pendente")
@pytest.mark.parametrize("country,label,receipt,currency,amount", [
    ("US", "Delivery 42", "Receipt 42", "USD", 11),
    ("PT", "Entrega 42", "Recibo 42", "EUR", 10),
])
def test_regional_bundle(country, label, receipt, currency, amount):
    bundle = api.prepare(country, "42", 2)
    assert bundle == {
        "label": {"country": country, "text": label},
        "receipt": {"country": country, "text": receipt},
        "freight": {"country": country, "currency": currency, "amount": amount},
    }


@pytest.mark.xfail(strict=True, reason="Alternância de países pendente")
def test_regions_do_not_leak_between_requests():
    for country in ["US", "BR", "PT", "US"]:
        bundle = api.prepare(country, "42", 1)
        assert {part["country"] for part in bundle.values()} == {country}


@pytest.mark.xfail(strict=True, reason="Entradas regionais individuais pendentes")
@pytest.mark.parametrize("country", ["US", "PT"])
def test_individual_entries_match_bundle(country):
    bundle = api.prepare(country, "42", 2)
    assert api.label(country, "42") == bundle["label"]
    assert api.receipt(country, "42") == bundle["receipt"]
    assert api.freight(country, 2) == bundle["freight"]

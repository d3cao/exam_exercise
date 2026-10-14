import json
import pytest
from aurora import d06_legacy as api


def test_modern_contract():
    assert api.ship({"order_id": "42", "weight": 2, "postal_code": "50000"}, api.ModernCarrier()) == {"tracking": "MOD-42", "status": "accepted"}


def test_modern_invalid_weight():
    with pytest.raises(ValueError):
        api.ship({"order_id": "42", "weight": 0, "postal_code": "50000"}, api.ModernCarrier())


def test_legacy_native_contract():
    carrier = api.LegacyCarrier()
    assert "LEG-42" in carrier.submit("42|2|50000")
    assert carrier.requests == ["42|2|50000"]


@pytest.mark.xfail(strict=True, reason="Integração do fornecedor legado pendente")
@pytest.mark.parametrize("order_id,weight", [("42", 2), ("A&B", 1.5)])
def test_legacy_through_current_contract(order_id, weight):
    carrier = api.LegacyCarrier()
    payload = {"order_id": order_id, "weight": weight, "postal_code": "05000"}
    result = api.ship(payload, carrier)
    assert result == {"tracking": f"LEG-{order_id}", "status": "accepted"}
    assert json.loads(json.dumps(result)) == result
    assert carrier.requests == [f"{order_id}|{weight}|05000"]
    assert payload == {"order_id": order_id, "weight": weight, "postal_code": "05000"}


@pytest.mark.xfail(strict=True, reason="Validação antes da integração pendente")
@pytest.mark.parametrize("field,value", [("weight", 0), ("order_id", "A|B"), ("postal_code", "50|000")])
def test_invalid_legacy_payload_never_submitted(field, value):
    carrier = api.LegacyCarrier()
    payload = {"order_id": "42", "weight": 2, "postal_code": "50000"}
    payload[field] = value
    with pytest.raises(ValueError):
        api.ship(payload, carrier)
    assert carrier.requests == []

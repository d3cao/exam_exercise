from copy import deepcopy
import pytest
from aurora import d08_cargo as api


def item(weight=2, price=10):
    return {"kind": "item", "weight": weight, "price": price}


@pytest.mark.parametrize("cargo,result", [(item(), {"weight": 2, "price": 10}), ({"kind": "box", "children": [item(), item(3, 20)]}, {"weight": 5, "price": 30}), ({"kind": "box", "children": []}, {"weight": 0, "price": 0})])
def test_existing_totals(cargo, result):
    assert api.totals(cargo) == result


def test_negative_item():
    with pytest.raises(ValueError):
        api.totals(item(-1))


@pytest.mark.xfail(strict=True, reason="Agrupamentos aninhados pendentes")
@pytest.mark.parametrize("kind", ["box", "pallet"])
def test_nested_groups(kind):
    cargo = {"kind": kind, "children": [item(), {"kind": "box", "children": [item(3, 20), {"kind": "box", "children": []}]}]}
    original = deepcopy(cargo)
    assert api.totals(cargo) == {"weight": 5, "price": 30}
    assert cargo == original


@pytest.mark.xfail(strict=True, reason="Validação uniforme dentro dos grupos pendente")
@pytest.mark.parametrize("bad", [item(-1), item(1, -2), {"kind": "unknown", "weight": 1, "price": 1}])
def test_invalid_child(bad):
    with pytest.raises(ValueError):
        api.totals({"kind": "box", "children": [bad]})


@pytest.mark.xfail(strict=True, reason="Pallet vazio pendente")
def test_empty_pallet():
    assert api.totals({"kind": "pallet", "children": []}) == {"weight": 0, "price": 0}

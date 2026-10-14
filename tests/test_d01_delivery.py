import pytest
from aurora import d01_delivery as api


@pytest.mark.parametrize("mode,amount,prefix,vehicle", [("road", 14, "ROAD", "truck"), ("air", 40, "AIR", "plane")])
def test_existing_flows(mode, amount, prefix, vehicle):
    assert api.quote(mode, 2) == amount
    code = api.dispatch(mode, "42")
    assert code == f"{prefix}-42"
    assert api.track(mode, code) == {"code": code, "vehicle": vehicle}


@pytest.mark.parametrize("weight", [0, -1])
def test_invalid_weight(weight):
    with pytest.raises(ValueError):
        api.quote("road", weight)


@pytest.mark.parametrize("operation,args", [(api.quote, ("sea", 2)), (api.dispatch, ("sea", "42")), (api.track, ("sea", "42"))])
def test_unknown_mode(operation, args):
    with pytest.raises(ValueError):
        operation(*args)


@pytest.mark.xfail(strict=True, reason="Entrega por bicicleta pendente")
@pytest.mark.parametrize("weight", [1, 3, 10])
def test_bicycle_flows(weight):
    assert api.quote("bike", weight) == 4 + weight
    code = api.dispatch("bike", "42")
    assert code == "BIKE-42"
    assert api.track("bike", code) == {"code": code, "vehicle": "bicycle"}

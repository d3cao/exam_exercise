import pytest
from aurora import d10_dispatch as api

STEPS = ["stock", "payment", "label", "collection"]


def test_manual_dispatch():
    operations = api.Operations()
    assert api.manual_dispatch("42", operations) == {"label": "LABEL-42", "pickup": "PICKUP-42"}
    assert operations.events == [(step, "42") for step in STEPS]


@pytest.mark.parametrize("step", STEPS)
def test_manual_stops_after_failure(step):
    operations = api.Operations(fail_at=step)
    with pytest.raises(RuntimeError):
        api.manual_dispatch("42", operations)
    assert operations.events == [(name, "42") for name in STEPS[:STEPS.index(step) + 1]]


@pytest.mark.xfail(strict=True, reason="Entrada de despacho coordenado pendente")
@pytest.mark.parametrize("order_id", ["42", "43"])
def test_dispatch_entrypoint(order_id):
    operations = api.Operations()
    assert api.dispatch(order_id, operations) == {"label": f"LABEL-{order_id}", "pickup": f"PICKUP-{order_id}"}
    assert operations.events == [(step, order_id) for step in STEPS]


@pytest.mark.xfail(strict=True, reason="Propagação de falhas no despacho coordenado pendente")
@pytest.mark.parametrize("step", STEPS)
def test_dispatch_failure(step):
    operations = api.Operations(fail_at=step)
    with pytest.raises(RuntimeError, match=f"Falha em {step}"):
        api.dispatch("42", operations)
    assert operations.events == [(name, "42") for name in STEPS[:STEPS.index(step) + 1]]

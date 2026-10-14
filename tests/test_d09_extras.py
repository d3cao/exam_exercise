import itertools
import pytest
from aurora import d09_extras as api


@pytest.mark.parametrize("extras,total,lines", [((), 20, [("base", 20)]), (("insurance",), 25, [("base", 20), ("insurance", 5)]), (("priority",), 32, [("base", 20), ("priority", 12)])])
def test_existing_quotes(extras, total, lines):
    assert api.quote(20, extras) == {"total": total, "lines": lines}


@pytest.mark.parametrize("base,extras", [(-1, ()), (20, ("unknown",))])
def test_invalid_input(base, extras):
    with pytest.raises(ValueError):
        api.quote(base, extras)


@pytest.mark.xfail(strict=True, reason="Combinação livre dos adicionais pendente")
@pytest.mark.parametrize("extras", list(itertools.permutations(["insurance", "priority", "notification"])) + [("notification",), ("priority", "insurance")])
def test_combinations(extras):
    fees = {"insurance": 5, "priority": 12, "notification": 2}
    assert api.quote(20, extras) == {"total": 20 + sum(fees[name] for name in extras), "lines": [("base", 20)] + [(name, fees[name]) for name in extras]}
    assert api.quote(20) == {"total": 20, "lines": [("base", 20)]}


def test_duplicate_extra_rejected():
    with pytest.raises(ValueError):
        api.quote(20, ("insurance", "insurance"))

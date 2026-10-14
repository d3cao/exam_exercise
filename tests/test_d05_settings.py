import importlib
import pytest
from aurora import d05_settings as api


@pytest.fixture(autouse=True)
def fresh_module():
    importlib.reload(api)
    yield
    importlib.reload(api)


def test_defaults():
    settings = api.get_settings()
    assert (settings.currency, settings.max_weight) == ("BRL", 30)


def test_invalid_update_is_rejected():
    settings = api.get_settings()
    with pytest.raises(ValueError):
        settings.update(currency="USD", max_weight=0)
    assert (settings.currency, settings.max_weight) == ("BRL", 30)


@pytest.mark.xfail(strict=True, reason="Configuração única entre serviços pendente")
def test_services_observe_same_configuration():
    quote, dispatch = api.QuoteService(), api.DispatchService()
    quote.settings.update(currency="USD", max_weight=50)
    assert dispatch.settings is quote.settings is api.get_settings()
    assert (dispatch.settings.currency, dispatch.settings.max_weight) == ("USD", 50)


@pytest.mark.xfail(strict=True, reason="Inicialização única pendente")
def test_configuration_loaded_once():
    for _ in range(10):
        api.get_settings()
        api.QuoteService()
        api.DispatchService()
    assert api.Settings.loads == 1

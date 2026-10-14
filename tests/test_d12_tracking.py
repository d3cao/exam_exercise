import pytest
from aurora.d12_tracking import ProviderLoader, Tracking


def test_existing_lookup():
    loader = ProviderLoader()
    tracking = Tracking(loader)
    assert tracking.lookup("42") == {"code": "42", "status": "in_transit"}
    assert loader.instance.calls == ["42"]


def test_provider_failure_propagates():
    loader = ProviderLoader()
    tracking = Tracking(loader)
    tracking.lookup("setup")
    loader.instance.fail_next = True
    with pytest.raises(ConnectionError):
        tracking.lookup("42")


@pytest.mark.xfail(strict=True, reason="Carregamento sob demanda pendente")
def test_lazy_initialization():
    loader = ProviderLoader()
    tracking = Tracking(loader)
    assert loader.loads == 0
    tracking.lookup("42")
    tracking.lookup("43")
    assert loader.loads == 1


@pytest.mark.xfail(strict=True, reason="Autorização antes de inicializar pendente")
def test_unauthorized_request_does_not_initialize():
    loader = ProviderLoader()
    tracking = Tracking(loader)
    with pytest.raises(PermissionError):
        tracking.lookup("42", authorized=False)
    assert loader.loads == 0


@pytest.mark.xfail(strict=True, reason="Cache de sucesso e proteção dos resultados pendentes")
def test_cached_results_are_independent():
    loader = ProviderLoader()
    tracking = Tracking(loader)
    first = tracking.lookup("42")
    first["status"] = "tampered"
    assert tracking.lookup("42") == {"code": "42", "status": "in_transit"}
    tracking.lookup("43")
    assert loader.instance.calls == ["42", "43"]


@pytest.mark.xfail(strict=True, reason="Autorização antes de consultar cache pendente")
def test_cached_result_still_requires_permission():
    loader = ProviderLoader()
    tracking = Tracking(loader)
    tracking.lookup("42")
    with pytest.raises(PermissionError):
        tracking.lookup("42", authorized=False)
    assert loader.instance.calls == ["42"]


@pytest.mark.xfail(strict=True, reason="Cache não deve armazenar falhas pendente")
def test_failed_request_can_be_retried_and_success_cached():
    loader = ProviderLoader()
    tracking = Tracking(loader)
    tracking.lookup("setup")
    loader.instance.fail_next = True
    with pytest.raises(ConnectionError):
        tracking.lookup("42")
    assert tracking.lookup("42")["status"] == "in_transit"
    assert tracking.lookup("42")["status"] == "in_transit"
    assert loader.instance.calls == ["setup", "42", "42"]


@pytest.mark.xfail(strict=True, reason="Caches independentes por serviço pendentes")
def test_cache_belongs_to_each_tracking_service():
    first_loader, second_loader = ProviderLoader(), ProviderLoader()
    first, second = Tracking(first_loader), Tracking(second_loader)
    first.lookup("42")
    first.lookup("42")
    second.lookup("42")
    second.lookup("42")
    assert first_loader.instance.calls == second_loader.instance.calls == ["42"]
    assert first_loader.loads == second_loader.loads == 1

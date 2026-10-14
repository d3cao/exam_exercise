import pytest
from aurora import d07_documents as api

ORDER = {"id": "42", "recipient": "Ana"}


@pytest.mark.parametrize("kind,channel,result", [("label", "text", "Etiqueta: 42 - Ana"), ("label", "html", "<p>Etiqueta: 42 - Ana</p>"), ("receipt", "text", "Comprovante: 42 - Ana")])
def test_existing_documents(kind, channel, result):
    assert api.render(kind, channel, ORDER) == result


@pytest.mark.parametrize("kind,channel", [("unknown", "text"), ("label", "pdf")])
def test_unknown_document_or_channel(kind, channel):
    with pytest.raises(ValueError):
        api.render(kind, channel, ORDER)


@pytest.mark.xfail(strict=True, reason="Novas combinações de documento e canal pendentes")
@pytest.mark.parametrize("kind,channel,result", [("receipt", "html", "<p>Comprovante: 42 - Ana</p>"), ("manifest", "text", "Manifesto: 42 - Ana"), ("manifest", "html", "<p>Manifesto: 42 - Ana</p>")])
def test_new_combinations(kind, channel, result):
    assert api.render(kind, channel, ORDER) == result


@pytest.mark.xfail(strict=True, reason="Escape HTML em novos documentos pendente")
@pytest.mark.parametrize("kind,prefix", [("receipt", "Comprovante"), ("manifest", "Manifesto")])
def test_html_escape(kind, prefix):
    assert api.render(kind, "html", {"id": "A&B", "recipient": "<Ana>"}) == f"<p>{prefix}: A&amp;B - &lt;Ana&gt;</p>"

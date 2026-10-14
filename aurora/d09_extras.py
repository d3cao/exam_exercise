"""Tarifas de serviços adicionais calculadas como combinações fechadas."""


def quote(base, extras=()):
    if base < 0:
        raise ValueError("Preço base não pode ser negativo")
    extras = tuple(extras)
    if not extras:
        return {"total": base, "lines": [("base", base)]}
    if extras == ("insurance",):
        return {"total": base + 5, "lines": [("base", base), ("insurance", 5)]}
    if extras == ("priority",):
        return {"total": base + 12, "lines": [("base", base), ("priority", 12)]}
    raise ValueError("Combinação de serviços indisponível")

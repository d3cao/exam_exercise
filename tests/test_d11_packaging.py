from dataclasses import FrozenInstanceError
import pytest
from aurora.d11_packaging import Warehouse


def test_package_fields_and_ownership():
    contents = ["BOOK"]
    package = Warehouse().create("1", "cardboard", (10, 20, 30), "A1", contents)
    contents.append("KIT")
    assert (package.identifier, package.position, package.contents) == ("1", "A1", ["BOOK"])
    assert package.specification.material == "cardboard"
    with pytest.raises(FrozenInstanceError):
        package.specification.width = 99


@pytest.mark.parametrize("dimensions", [(0, 1, 1), (-1, 1, 1), (1, 1)])
def test_invalid_dimensions(dimensions):
    with pytest.raises(ValueError):
        Warehouse().create("1", "cardboard", dimensions, "A1", [])


def test_catalogs_belong_to_each_warehouse():
    first, second = Warehouse(), Warehouse()
    a = first.create("1", "cardboard", (10, 20, 30), "A", [])
    b = second.create("2", "cardboard", (10, 20, 30), "B", [])
    assert a.specification is not b.specification
    assert first.specifications_created == second.specifications_created == 1


@pytest.mark.xfail(strict=True, reason="Reutilização do catálogo pendente")
def test_thousand_packages_share_specification():
    warehouse = Warehouse()
    packages = [warehouse.create(str(i), "cardboard", (10, 20, 30), f"A{i}", [str(i)]) for i in range(1000)]
    assert warehouse.specifications_created == 1
    assert all(package.specification is packages[0].specification for package in packages)
    packages[0].contents.append("KIT")
    packages[0].position = "B1"
    assert packages[1].contents == ["1"]
    assert packages[1].position == "A1"
    assert len({package.identifier for package in packages}) == 1000


@pytest.mark.xfail(strict=True, reason="Chave completa do catálogo pendente")
def test_material_and_all_dimensions_identify_specification():
    warehouse = Warehouse()
    inputs = [("cardboard", (10, 20, 30)), ("plastic", (10, 20, 30)), ("cardboard", (11, 20, 30)), ("cardboard", (10, 21, 30)), ("cardboard", (10, 20, 31))]
    first = [warehouse.create(str(i), material, dimensions, "A", []) for i, (material, dimensions) in enumerate(inputs)]
    second = [warehouse.create(str(i), material, list(dimensions), "B", []) for i, (material, dimensions) in enumerate(inputs)]
    assert warehouse.specifications_created == 5
    assert len({id(package.specification) for package in first}) == 5
    assert all(a.specification is b.specification for a, b in zip(first, second))

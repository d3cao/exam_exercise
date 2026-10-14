"""Especificações idênticas reconstruídas para cada embalagem física."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Specification:
    material: str
    width: int
    height: int
    depth: int


@dataclass
class Package:
    identifier: str
    specification: Specification
    position: str
    contents: list


class Warehouse:
    def __init__(self):
        self.specifications_created = 0

    def create(self, identifier, material, dimensions, position, contents):
        if len(dimensions) != 3 or any(size <= 0 for size in dimensions):
            raise ValueError("Dimensões devem ser três valores positivos")
        self.specifications_created += 1
        spec = Specification(material, *dimensions)
        return Package(identifier, spec, position, list(contents))

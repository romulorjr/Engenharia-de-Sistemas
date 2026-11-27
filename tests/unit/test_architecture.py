"""ENG-DOC, ENG-QUAL (#3): separação de camadas exigida pelo PDF (seção 3).

Lê cada módulo de ``src/maquina_cafe`` com ``ast`` e falha se ele importar algo
proibido para a sua camada (tabela no design da #3 e no steering). Falha aqui é
regressão real (ADR 0006): corrige-se o código, não a tabela.
"""

import ast
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
PACKAGE = SRC / "maquina_cafe"
LAYERS = ("api", "services", "domain", "persistence")

WEB = ("fastapi", "starlette")
DATABASE = ("sqlalchemy", "alembic")
FORBIDDEN: dict[str, tuple[str, ...]] = {
    "domain": (
        *WEB,
        "pydantic",
        *DATABASE,
        "maquina_cafe.api",
        "maquina_cafe.services",
        "maquina_cafe.persistence",
    ),
    "services": (*WEB, *DATABASE, "maquina_cafe.api"),
    "persistence": (*WEB, "maquina_cafe.api", "maquina_cafe.services"),
    "api": DATABASE,
    # Módulos fora das camadas (__init__ do pacote, config): sem framework nem banco.
    "root": (*WEB, *DATABASE),
}


def module_name(path: Path) -> str:
    """Nome do módulo Python de um arquivo em ``src/``."""
    parts = list(path.relative_to(SRC).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def layer_of(path: Path) -> str:
    """Camada do arquivo: primeira pasta abaixo de ``maquina_cafe`` ou ``root``."""
    parts = path.relative_to(PACKAGE).parts
    return parts[0] if len(parts) > 1 and parts[0] in LAYERS else "root"


def imported_modules(source: str, module: str, is_package: bool) -> list[tuple[int, str]]:
    """Módulos importados por ``source``, com imports relativos convertidos em absolutos.

    Para ``from x import y`` devolve ``x`` e ``x.y``, porque ``y`` pode ser um
    submódulo (ex.: ``from maquina_cafe import api``).
    """
    package = module.split(".") if is_package else module.split(".")[:-1]
    found: list[tuple[int, str]] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package[: len(package) - (node.level - 1)]
                target = ".".join([*base, node.module] if node.module else base)
            else:
                target = node.module or ""
            found.append((node.lineno, target))
            found.extend((node.lineno, f"{target}.{alias.name}") for alias in node.names)
    return found


def violations(source: str, module: str, layer: str, is_package: bool) -> list[str]:
    """Imports de ``source`` proibidos para ``layer``."""
    forbidden = FORBIDDEN[layer]
    return sorted(
        {
            f"linha {line}: {name}"
            for line, name in imported_modules(source, module, is_package)
            if any(name == prefix or name.startswith(f"{prefix}.") for prefix in forbidden)
        }
    )


SOURCE_FILES = sorted(PACKAGE.rglob("*.py"))


def test_every_layer_package_exists():
    """As quatro camadas existem como pacotes; sem isso o teste abaixo seria vazio."""
    for layer in LAYERS:
        assert (PACKAGE / layer / "__init__.py").is_file(), layer
    assert SOURCE_FILES


@pytest.mark.parametrize("path", SOURCE_FILES, ids=lambda p: p.relative_to(SRC).as_posix())
def test_module_respects_layer_imports(path):
    """Nenhum módulo importa o que a sua camada proíbe."""
    found = violations(
        path.read_text(encoding="utf-8"),
        module_name(path),
        layer_of(path),
        is_package=path.name == "__init__.py",
    )
    assert not found, f"{path.relative_to(SRC)} ({layer_of(path)}): {found}"


@pytest.mark.parametrize(
    ("source", "module", "layer", "expected"),
    [
        ("import fastapi", "maquina_cafe.domain.receita", "domain", ["linha 1: fastapi"]),
        (
            "from sqlalchemy.orm import Session",
            "maquina_cafe.services.pedido",
            "services",
            ["linha 1: sqlalchemy.orm", "linha 1: sqlalchemy.orm.Session"],
        ),
        (
            "from ..api import app",
            "maquina_cafe.domain.receita",
            "domain",
            ["linha 1: maquina_cafe.api", "linha 1: maquina_cafe.api.app"],
        ),
        (
            "from maquina_cafe import services",
            "maquina_cafe.persistence.x",
            "persistence",
            [
                "linha 1: maquina_cafe.services",
            ],
        ),
        ("import fastapi", "maquina_cafe.api.app", "api", []),
        ("from fastapi_extra import x", "maquina_cafe.domain.receita", "domain", []),
    ],
)
def test_violations_detects_forbidden_imports(source, module, layer, expected):
    """O detector reconhece imports absolutos, relativos e de submódulos."""
    assert violations(source, module, layer, is_package=False) == expected


def test_relative_import_from_package_init():
    """Em ``__init__.py``, ``from . import x`` resolve para o próprio pacote."""
    found = imported_modules("from . import app", "maquina_cafe.api", is_package=True)
    assert (1, "maquina_cafe.api.app") in found

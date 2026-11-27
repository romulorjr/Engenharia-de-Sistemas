"""Fixtures comuns a todos os testes.

Este arquivo não importa FastAPI, para que os testes unitários rodem sem a
camada HTTP. Fixtures que dependem de FastAPI ficam em
``tests/integration/conftest.py``.
"""

import pytest

from maquina_cafe.config import Settings


@pytest.fixture
def settings(tmp_path) -> Settings:
    """Configuração de teste com banco em arquivo temporário (ADR 0006)."""
    return Settings(database_url=f"sqlite:///{tmp_path / 'maquina_cafe_test.db'}")

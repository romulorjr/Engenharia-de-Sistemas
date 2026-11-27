"""Fixtures dos testes de integração (aplicação FastAPI completa)."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from maquina_cafe.api.app import create_app
from maquina_cafe.config import Settings


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    """Cliente HTTP da aplicação criada com a configuração de teste."""
    with TestClient(create_app(settings)) as test_client:
        yield test_client

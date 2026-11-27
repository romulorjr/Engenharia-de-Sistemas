"""ENG-INFRA (#2): a aplicação inicia e publica a documentação da API."""

import importlib
import tomllib
from pathlib import Path

import pytest

import maquina_cafe.api.app as app_module
from maquina_cafe import __version__
from maquina_cafe.api.app import create_app
from maquina_cafe.config import DATABASE_URL_ENV, InvalidSettingsError

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def test_app_startup(client):
    """/openapi.json e /docs respondem 200, com título e versão do pyproject."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    info = response.json()["info"]
    assert info["title"] == "Máquina de Café ESI"
    declared = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["version"]
    assert info["version"] == declared == __version__

    docs = client.get("/docs")
    assert docs.status_code == 200
    assert "swagger-ui" in docs.text


def test_create_app_uses_given_settings(monkeypatch, settings):
    """Configuração explícita é usada, mesmo com o ambiente diferente."""
    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite:///ignorado.db")
    app = create_app(settings)
    assert app.state.settings is settings


def test_create_app_reads_environment_without_settings(monkeypatch):
    """Sem configuração explícita, create_app lê as variáveis de ambiente."""
    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite:///ambiente.db")
    app = create_app()
    assert app.state.settings.database_url == "sqlite:///ambiente.db"


def test_create_app_rejects_invalid_environment(monkeypatch):
    """Variável vazia no ambiente impede a criação da aplicação."""
    monkeypatch.setenv(DATABASE_URL_ENV, "")
    with pytest.raises(InvalidSettingsError, match=DATABASE_URL_ENV):
        create_app()


def test_importing_app_module_has_no_side_effects(monkeypatch):
    """Importar o módulo não cria a aplicação nem lê o ambiente."""
    monkeypatch.setenv(DATABASE_URL_ENV, "")
    reloaded = importlib.reload(app_module)
    assert not hasattr(reloaded, "app")

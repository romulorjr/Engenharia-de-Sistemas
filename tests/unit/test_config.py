"""ENG-INFRA (#2): configuração por variáveis de ambiente."""

import dataclasses

import pytest

from maquina_cafe.config import (
    DATABASE_URL_ENV,
    DEFAULT_DATABASE_URL,
    InvalidSettingsError,
    Settings,
)


def test_settings_default_database_url():
    """Variável ausente usa o banco SQLite padrão."""
    assert Settings.from_env({}).database_url == "sqlite:///maquina_cafe.db"
    assert DEFAULT_DATABASE_URL == "sqlite:///maquina_cafe.db"


def test_settings_reads_environment():
    """O valor de MAQUINA_CAFE_DATABASE_URL é usado sem alteração."""
    environ = {DATABASE_URL_ENV: "sqlite:///outro.db"}
    assert Settings.from_env(environ).database_url == "sqlite:///outro.db"


def test_settings_reads_process_environment_by_default(monkeypatch):
    """Sem mapeamento explícito, from_env lê os.environ."""
    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite:///processo.db")
    assert Settings.from_env().database_url == "sqlite:///processo.db"


@pytest.mark.parametrize("value", ["", " ", "\t\n"])
def test_settings_rejects_empty_value(value):
    """Variável definida e vazia (ou só espaços) impede a criação da configuração."""
    with pytest.raises(InvalidSettingsError, match=DATABASE_URL_ENV):
        Settings.from_env({DATABASE_URL_ENV: value})


def test_settings_is_immutable(settings):
    """A configuração não muda depois de criada."""
    with pytest.raises(dataclasses.FrozenInstanceError):
        settings.database_url = "sqlite:///alterado.db"  # type: ignore[misc]

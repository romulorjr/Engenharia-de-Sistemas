"""Configuração da aplicação, lida de variáveis de ambiente.

Variáveis documentadas em ``.env.example``. A aplicação não lê arquivos
``.env``: os valores vêm do ambiente do processo.
"""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

DATABASE_URL_ENV = "MAQUINA_CAFE_DATABASE_URL"
DEFAULT_DATABASE_URL = "sqlite:///maquina_cafe.db"


class InvalidSettingsError(ValueError):
    """Variável de ambiente definida com valor inválido."""


@dataclass(frozen=True)
class Settings:
    """Configuração imutável da aplicação.

    ``database_url`` é a URL do banco no formato do SQLAlchemy. Nesta versão
    ela só é guardada; a persistência a usa a partir da issue #4.
    """

    database_url: str = DEFAULT_DATABASE_URL

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Self:
        """Cria a configuração a partir de ``environ`` (padrão: ``os.environ``).

        Variável ausente usa o valor padrão. Variável definida com valor vazio
        ou só com espaços gera ``InvalidSettingsError``.
        """
        env = os.environ if environ is None else environ
        return cls(database_url=_read(env, DATABASE_URL_ENV, DEFAULT_DATABASE_URL))


def _read(env: Mapping[str, str], name: str, default: str) -> str:
    value = env.get(name)
    if value is None:
        return default
    if not value.strip():
        raise InvalidSettingsError(f"{name} não pode ser vazia.")
    return value

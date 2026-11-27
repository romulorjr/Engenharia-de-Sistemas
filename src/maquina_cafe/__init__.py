"""Back-end da máquina de café automática (disciplina ESI).

Camadas, de fora para dentro:

- ``api``: controllers HTTP e ponto de composição da aplicação;
- ``services``: regras de negócio RN01 a RN12 e fronteiras de transação;
- ``domain``: entidades, receitas, estados e valores, sem framework;
- ``persistence``: modelos, repositories e migrações do banco.

A versão vem dos metadados do pacote instalado, com uma única fonte no
``pyproject.toml``.
"""

from importlib.metadata import version

__version__ = version("maquina-cafe")

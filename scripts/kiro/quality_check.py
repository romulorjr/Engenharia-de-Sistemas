"""Executa lint, formatação e testes quando o projeto Python já existe.

Usado pelos hooks `.kiro/hooks/quality-on-save.json` (`--lint-only`) e
`.kiro/hooks/quality-on-stop.json` (`--if-changed`). Também pode ser executado
manualmente: `python scripts/kiro/quality_check.py [--lint-only] [--if-changed]`.

- `--lint-only`: executa apenas Ruff (lint e formatação).
- `--if-changed`: só executa se houver alteração não commitada em `src/`,
  `tests/` ou `pyproject.toml`.

Enquanto `pyproject.toml` não existir (issue #2), não há o que verificar e o
script termina com sucesso. Ferramentas ausentes são relatadas como falha, para
que o ambiente seja corrigido em vez de o problema passar despercebido.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

WATCHED = ("src/", "tests/", "pyproject.toml")


def _has_pending_code_changes() -> bool:
    status = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, check=False
    )
    paths = [line[3:].strip() for line in status.stdout.splitlines()]
    return any(path.startswith(WATCHED) for path in paths)


def _run(label: str, command: list[str]) -> bool:
    if shutil.which(command[0]) is None and command[0] != sys.executable:
        print(f"[{label}] ferramenta ausente: {command[0]}", file=sys.stderr)
        return False
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip().splitlines()
        print(f"[{label}] falhou:", file=sys.stderr)
        print("\n".join(output[-40:]), file=sys.stderr)
        return False
    return True


def main(argv: list[str]) -> int:
    if not Path("pyproject.toml").exists():
        return 0
    if "--if-changed" in argv and not _has_pending_code_changes():
        return 0
    checks = [
        ("ruff check", ["ruff", "check", "."]),
        ("ruff format", ["ruff", "format", "--check", "."]),
    ]
    if "--lint-only" not in argv:
        checks.append(("pytest", [sys.executable, "-m", "pytest", "-q"]))
    results = [_run(label, command) for label, command in checks]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

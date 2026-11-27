"""Verifica se mudanças de código vieram acompanhadas da documentação obrigatória.

Usado pelo hook `.kiro/hooks/docs-guard.json` (gatilho Stop) e pode ser executado
manualmente: `python scripts/kiro/docs_guard.py`.

Compara a árvore de trabalho com o ponto em que a branch saiu de `origin/main`
(inclui commits da branch, alterações não commitadas e arquivos novos). Se algum
arquivo em `src/` ou `tests/` mudou e `CHANGELOG.md` ou `docs/CONTEXT.md` não,
termina com código 1 e explica o que falta em stderr.
"""

from __future__ import annotations

import subprocess
import sys

CODE_PREFIXES = ("src/", "tests/")
REQUIRED_DOCS = ("CHANGELOG.md", "docs/CONTEXT.md")
CHECK_ALSO = (
    "docs/rastreabilidade.md",
    "README.md (endpoints, comandos, status)",
    "docs/api/ (OpenAPI/Postman) se a API mudou",
    "docs/arquitetura.md (diagrama) se classes ou camadas mudaram",
    "docs/quality-report.md e docs/contributions.md",
)


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False)


def changed_files() -> set[str]:
    base = _git("merge-base", "HEAD", "origin/main").stdout.strip() or "HEAD"
    diff = _git("diff", "--name-only", base).stdout.splitlines()
    untracked = _git("ls-files", "--others", "--exclude-standard").stdout.splitlines()
    return {path.strip() for path in diff + untracked if path.strip()}


def main() -> int:
    if _git("rev-parse", "--is-inside-work-tree").returncode != 0:
        return 0
    files = changed_files()
    code = sorted(
        path for path in files if path.startswith(CODE_PREFIXES) and not path.endswith(".gitkeep")
    )
    if not code:
        return 0
    missing = [doc for doc in REQUIRED_DOCS if doc not in files]
    if not missing:
        return 0
    print(
        "Código alterado sem a documentação obrigatória.\n"
        f"Arquivos de código: {', '.join(code[:10])}\n"
        f"Atualize: {', '.join(missing)}.\n"
        f"Verifique também: {'; '.join(CHECK_ALSO)}.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())

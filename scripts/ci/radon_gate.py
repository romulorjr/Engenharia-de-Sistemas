"""Limites de complexidade e manutenibilidade (Radon) para a CI.

Uso, na raiz do repositório: ``python scripts/ci/radon_gate.py [pasta]`` (padrão: ``src``).

- Grava ``radon-cc.txt`` (``radon cc -s -a``), ``radon-mi.txt`` (``radon mi -s``)
  e ``radon-gate.json`` (avisos e falhas) na pasta atual.
- Falha (código 1) se algum bloco tiver complexidade ciclomática de classe D ou
  pior, ou algum módulo tiver índice de manutenibilidade abaixo da classe A.
- Emite aviso, sem falhar, para blocos de classe C.
- Código 2: o Radon não pôde ser executado.

Limites decididos em 27/11/2026 (ADR 0006, spec da #3). Não reduzir os limites
para a CI passar: corrigir os blocos apontados.
"""

import json
import os
import shutil
import subprocess
import sys
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path

CC_WARN_RANKS = frozenset({"C"})
CC_FAIL_RANKS = frozenset({"D", "E", "F"})
MI_REQUIRED_RANK = "A"


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    message: str


@dataclass
class GateResult:
    failures: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    def extend(self, other: "GateResult") -> None:
        self.failures.extend(other.failures)
        self.warnings.extend(other.warnings)


def _walk(blocks: list[dict]) -> Iterator[dict]:
    for block in blocks:
        yield block
        yield from _walk(block.get("closures") or [])


def _block_label(block: dict) -> str:
    name = block["name"]
    if block.get("classname") and block.get("type") == "method":
        name = f"{block['classname']}.{name}"
    return f"{block.get('type', 'bloco')} {name}"


def evaluate_cc(report: dict) -> GateResult:
    """Avalia a saída de ``radon cc -j``."""
    result = GateResult()
    for path, blocks in sorted(report.items()):
        if isinstance(blocks, dict):
            reason = blocks.get("error", "erro desconhecido")
            result.failures.append(Finding(path, 1, f"Radon não analisou o arquivo: {reason}"))
            continue
        for block in _walk(blocks):
            rank = block["rank"]
            text = f"{_block_label(block)}: complexidade {block['complexity']} (classe {rank})"
            finding = Finding(path, int(block.get("lineno", 1)), text)
            if rank in CC_FAIL_RANKS:
                result.failures.append(finding)
            elif rank in CC_WARN_RANKS:
                result.warnings.append(finding)
    return result


def evaluate_mi(report: dict) -> GateResult:
    """Avalia a saída de ``radon mi -j``."""
    result = GateResult()
    for path, data in sorted(report.items()):
        if "error" in data:
            result.failures.append(
                Finding(path, 1, f"Radon não analisou o arquivo: {data['error']}")
            )
        elif data["rank"] != MI_REQUIRED_RANK:
            text = (
                f"índice de manutenibilidade {float(data['mi']):.1f} "
                f"(classe {data['rank']}); mínimo: classe A"
            )
            result.failures.append(Finding(path, 1, text))
    return result


def _escape(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def annotation(level: str, finding: Finding) -> str:
    """Linha de anotação do GitHub Actions (``::error``/``::warning``)."""
    path = _escape(finding.path).replace(":", "%3A").replace(",", "%2C")
    return f"::{level} file={path},line={finding.line}::{_escape(finding.message)}"


def _radon_command() -> list[str]:
    executable = shutil.which("radon")
    return [executable] if executable else [sys.executable, "-m", "radon"]


def _run(command: list[str]) -> str:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        print(f"Falha ao executar {' '.join(command)}:\n{completed.stderr}", file=sys.stderr)
        raise SystemExit(2)
    return completed.stdout


def run_gate(target: str, output_dir: Path) -> GateResult:
    """Executa o Radon em ``target``, grava os relatórios e avalia os limites."""
    radon = _radon_command()
    (output_dir / "radon-cc.txt").write_text(_run([*radon, "cc", target, "-s", "-a"]), "utf-8")
    (output_dir / "radon-mi.txt").write_text(_run([*radon, "mi", target, "-s"]), "utf-8")
    result = evaluate_cc(json.loads(_run([*radon, "cc", target, "-j"])))
    result.extend(evaluate_mi(json.loads(_run([*radon, "mi", target, "-j"]))))
    payload = {
        "failures": [asdict(item) for item in result.failures],
        "warnings": [asdict(item) for item in result.warnings],
    }
    (output_dir / "radon-gate.json").write_text(json.dumps(payload, indent=2), "utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    result = run_gate(args[0] if args else "src", Path.cwd())
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for level, items in (("warning", result.warnings), ("error", result.failures)):
        for item in items:
            print(
                annotation(level, item)
                if in_actions
                else f"{level}: {item.path}:{item.line} {item.message}"
            )
    print(f"Radon: {len(result.failures)} falha(s), {len(result.warnings)} aviso(s) de classe C.")
    return 1 if result.failures else 0


if __name__ == "__main__":
    sys.exit(main())

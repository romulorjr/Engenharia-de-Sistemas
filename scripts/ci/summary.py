"""Resumo em Markdown da execução da CI.

Uso, na raiz do repositório depois das etapas da CI: ``python scripts/ci/summary.py``.
Lê ``pytest-junit.xml``, ``coverage.xml``, ``radon-cc.txt`` e ``radon-gate.json``
e as variáveis ``RESULT_*`` com o resultado de cada etapa. Arquivos ausentes
aparecem como "não disponível". Nunca falha: o resultado das etapas já define o
estado do job.
"""

import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

UNAVAILABLE = "não disponível"
STEPS = (
    ("Ruff (lint)", "RESULT_LINT"),
    ("Ruff (formatação)", "RESULT_FORMAT"),
    ("Testes e cobertura", "RESULT_TESTS"),
    ("Radon", "RESULT_RADON"),
    ("Fumaça (uvicorn)", "RESULT_SMOKE"),
)


def junit_counts(path: Path) -> dict[str, dict[str, int]]:
    """Testes por grupo (unit, integration, outros): total, falhas e ignorados."""
    counts: dict[str, dict[str, int]] = {}
    for case in ET.parse(path).getroot().iter("testcase"):
        classname = case.get("classname", "")
        group = next(
            (name for name in ("unit", "integration") if classname.startswith(f"tests.{name}.")),
            "outros",
        )
        bucket = counts.setdefault(group, {"total": 0, "falhas": 0, "ignorados": 0})
        bucket["total"] += 1
        if case.find("failure") is not None or case.find("error") is not None:
            bucket["falhas"] += 1
        elif case.find("skipped") is not None:
            bucket["ignorados"] += 1
    return counts


def coverage_rates(path: Path) -> dict[str, float | int]:
    """Cobertura de linhas e de ramos do relatório Cobertura (coverage.xml)."""
    root = ET.parse(path).getroot()
    return {
        "linhas": float(root.get("line-rate", 0)) * 100,
        "linhas_validas": int(root.get("lines-valid", 0)),
        "ramos": float(root.get("branch-rate", 0)) * 100,
        "ramos_validos": int(root.get("branches-valid", 0)),
    }


def average_complexity(text: str) -> str | None:
    """Média de complexidade da saída de ``radon cc -a`` (ex.: ``A (1.5)``)."""
    match = re.search(r"Average complexity:\s*([A-F])\s*\(([\d.]+)\)", text)
    return f"{match.group(1)} ({float(match.group(2)):.2f})" if match else None


def coverage_total() -> str:
    completed = subprocess.run(
        [sys.executable, "-m", "coverage", "report", "--format=total"],
        capture_output=True,
        text=True,
        check=False,
    )
    value = completed.stdout.strip()
    return f"{value}%" if completed.returncode == 0 and value else UNAVAILABLE


def render(base: Path, environ: dict[str, str], total: str) -> str:
    lines = ["## CI: testes e análise", "", "| Etapa | Resultado |", "|---|---|"]
    lines += [f"| {label} | {environ.get(var) or UNAVAILABLE} |" for label, var in STEPS]
    lines.append("")

    junit = base / "pytest-junit.xml"
    if junit.is_file():
        counts = junit_counts(junit)
        total_tests = sum(item["total"] for item in counts.values())
        parts = ", ".join(f"{name}: {item['total']}" for name, item in sorted(counts.items()))
        failed = sum(item["falhas"] for item in counts.values())
        skipped = sum(item["ignorados"] for item in counts.values())
        lines.append(f"- Testes: {total_tests} ({parts}); falhas: {failed}; ignorados: {skipped}")
    else:
        lines.append(f"- Testes: {UNAVAILABLE}")

    xml_report = base / "coverage.xml"
    if xml_report.is_file():
        rates = coverage_rates(xml_report)
        lines.append(
            f"- Cobertura total (critério do --cov-fail-under=75): {total}; "
            f"linhas {rates['linhas']:.1f}% de {rates['linhas_validas']}; "
            f"ramos {rates['ramos']:.1f}% de {rates['ramos_validos']}"
        )
    else:
        lines.append(f"- Cobertura: {UNAVAILABLE}")

    cc_text = base / "radon-cc.txt"
    average = average_complexity(cc_text.read_text("utf-8")) if cc_text.is_file() else None
    gate_file = base / "radon-gate.json"
    if gate_file.is_file():
        gate = json.loads(gate_file.read_text("utf-8"))
        lines.append(
            f"- Radon: CC média {average or UNAVAILABLE}; "
            f"avisos (classe C): {len(gate['warnings'])}; falhas: {len(gate['failures'])}"
        )
        lines += [
            f"  - {kind}: `{item['path']}:{item['line']}` {item['message']}"
            for kind, key in (("aviso", "warnings"), ("falha", "failures"))
            for item in gate[key]
        ]
    else:
        lines.append(f"- Radon: {UNAVAILABLE}")
    return "\n".join(lines) + "\n"


def main() -> int:
    print(render(Path.cwd(), dict(os.environ), coverage_total()), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""ENG-QUAL (#3): scripts da CI em ``scripts/ci``.

Os scripts ficam fora do pacote ``maquina_cafe`` e não entram na cobertura da
aplicação. Os testes de ``run_gate`` executam o Radon de verdade: na CI ele é
obrigatório; fora dela o teste é ignorado se o Radon não estiver instalado.
"""

import importlib.util
import json
import os
import sys
import textwrap
from pathlib import Path
from types import ModuleType

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts" / "ci"


def load_script(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"ci_{name}", SCRIPTS / f"{name}.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


radon_gate = load_script("radon_gate")
summary = load_script("summary")


def require_radon() -> None:
    if os.environ.get("CI"):
        import radon  # noqa: F401
    else:
        pytest.importorskip("radon")


def block(name: str, complexity: int, rank: str, **extra) -> dict:
    return {
        "type": "function",
        "name": name,
        "lineno": 3,
        "complexity": complexity,
        "rank": rank,
        **extra,
    }


# radon_gate: avaliação da complexidade ciclomática


@pytest.mark.parametrize("rank", ["A", "B"])
def test_cc_ranks_a_and_b_pass_silently(rank):
    result = radon_gate.evaluate_cc({"src/x.py": [block("f", 3, rank)]})
    assert result.failures == []
    assert result.warnings == []


def test_cc_rank_c_is_a_warning_not_a_failure():
    result = radon_gate.evaluate_cc({"src/x.py": [block("f", 11, "C")]})
    assert result.failures == []
    assert [w.message for w in result.warnings] == ["function f: complexidade 11 (classe C)"]
    assert result.warnings[0].line == 3


@pytest.mark.parametrize(("complexity", "rank"), [(21, "D"), (31, "E"), (41, "F")])
def test_cc_rank_d_or_worse_fails(complexity, rank):
    result = radon_gate.evaluate_cc({"src/x.py": [block("f", complexity, rank)]})
    assert result.warnings == []
    assert len(result.failures) == 1
    assert f"(classe {rank})" in result.failures[0].message


def test_cc_method_label_includes_class_and_closures_are_checked():
    method = block("calcular", 25, "D", type="method", classname="Pedido")
    outer = block("externa", 2, "A", closures=[block("interna", 12, "C")])
    result = radon_gate.evaluate_cc({"src/x.py": [method, outer]})
    assert [f.message for f in result.failures] == [
        "method Pedido.calcular: complexidade 25 (classe D)"
    ]
    assert [w.message for w in result.warnings] == ["function interna: complexidade 12 (classe C)"]


def test_cc_file_that_radon_cannot_parse_fails():
    result = radon_gate.evaluate_cc({"src/x.py": {"error": "invalid syntax"}})
    assert len(result.failures) == 1
    assert "invalid syntax" in result.failures[0].message


# radon_gate: avaliação do índice de manutenibilidade


def test_mi_rank_a_passes():
    assert radon_gate.evaluate_mi({"src/x.py": {"mi": 75.2, "rank": "A"}}).failures == []


@pytest.mark.parametrize(("mi", "rank"), [(15.0, "B"), (5.0, "C")])
def test_mi_below_rank_a_fails(mi, rank):
    result = radon_gate.evaluate_mi({"src/x.py": {"mi": mi, "rank": rank}})
    assert [f.message for f in result.failures] == [
        f"índice de manutenibilidade {mi:.1f} (classe {rank}); mínimo: classe A"
    ]


def test_mi_file_that_radon_cannot_parse_fails():
    result = radon_gate.evaluate_mi({"src/x.py": {"error": "invalid syntax"}})
    assert len(result.failures) == 1


def test_annotation_escapes_special_characters():
    finding = radon_gate.Finding("src/a,b:c.py", 7, "100% ruim\nsegunda linha")
    assert radon_gate.annotation("error", finding) == (
        "::error file=src/a%2Cb%3Ac.py,line=7::100%25 ruim%0Asegunda linha"
    )


# radon_gate: execução real do Radon


def _write_module(directory: Path, conditions: int) -> None:
    body = "\n".join(f"    if x == {i}:\n        return {i}" for i in range(conditions))
    (directory / "modulo.py").write_text(f"def ramificada(x):\n{body}\n    return -1\n", "utf-8")


def test_run_gate_fails_on_rank_d_function(tmp_path):
    require_radon()
    target = tmp_path / "pacote"
    target.mkdir()
    _write_module(target, conditions=20)  # CC 21: classe D
    result = radon_gate.run_gate(str(target), tmp_path)
    assert any("ramificada: complexidade 21 (classe D)" in f.message for f in result.failures)
    for report in ("radon-cc.txt", "radon-mi.txt", "radon-gate.json"):
        assert (tmp_path / report).is_file(), report
    saved = json.loads((tmp_path / "radon-gate.json").read_text("utf-8"))
    assert saved["failures"]


def test_run_gate_warns_on_rank_c_function(tmp_path):
    require_radon()
    target = tmp_path / "pacote"
    target.mkdir()
    _write_module(target, conditions=10)  # CC 11: classe C
    result = radon_gate.run_gate(str(target), tmp_path)
    assert not [f for f in result.failures if "complexidade" in f.message]
    assert any("ramificada: complexidade 11 (classe C)" in w.message for w in result.warnings)


# summary


def test_junit_counts_groups_by_test_folder(tmp_path):
    report = tmp_path / "pytest-junit.xml"
    report.write_text(
        textwrap.dedent(
            """\
            <testsuites><testsuite>
              <testcase classname="tests.unit.test_config" name="a"/>
              <testcase classname="tests.unit.test_config" name="b"><failure/></testcase>
              <testcase classname="tests.integration.test_app" name="c"><skipped/></testcase>
            </testsuite></testsuites>
            """
        ),
        "utf-8",
    )
    assert summary.junit_counts(report) == {
        "unit": {"total": 2, "falhas": 1, "ignorados": 0},
        "integration": {"total": 1, "falhas": 0, "ignorados": 1},
    }


def test_coverage_rates_reads_cobertura_attributes(tmp_path):
    report = tmp_path / "coverage.xml"
    report.write_text(
        '<coverage line-rate="0.9" branch-rate="0.5" lines-valid="20" branches-valid="4"/>',
        "utf-8",
    )
    rates = summary.coverage_rates(report)
    assert rates["linhas"] == pytest.approx(90.0)
    assert rates["ramos"] == pytest.approx(50.0)
    assert (rates["linhas_validas"], rates["ramos_validos"]) == (20, 4)


def test_average_complexity_parses_radon_output():
    text = "src/x.py\n    F 1:0 f - A (1)\n\n1 blocks (classes, functions, methods) analyzed.\n"
    assert summary.average_complexity(text + "Average complexity: A (1.5)\n") == "A (1.50)"
    assert summary.average_complexity("No blocks analyzed") is None


def test_render_marks_missing_reports_as_unavailable(tmp_path):
    text = summary.render(tmp_path, {"RESULT_LINT": "success"}, "n/d")
    assert "| Ruff (lint) | success |" in text
    assert "| Radon | não disponível |" in text
    assert "- Testes: não disponível" in text

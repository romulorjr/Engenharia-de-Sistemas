"""Teste propositalmente quebrado para provar que a CI falha (spec da #3, tarefa 5).

Revertido no commit seguinte.
"""


def test_ci_failure_probe():
    assert sum([1, 1]) == 3, "falha proposital"

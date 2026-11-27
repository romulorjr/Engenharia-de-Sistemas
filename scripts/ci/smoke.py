"""Teste de fumaça: a API inicia com uvicorn e responde 200 em /openapi.json.

Uso, na raiz do repositório e com o projeto instalado: ``python scripts/ci/smoke.py``.
Falha (código 1) se não houver resposta 200 em até 15 segundos e mostra a saída
do servidor.
"""

import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

APP = "maquina_cafe.api.app:create_app"
TIMEOUT_SECONDS = 15.0


def free_port() -> int:
    """Porta TCP livre em 127.0.0.1."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_ok(url: str, process: subprocess.Popen, timeout: float) -> bool:
    """Consulta ``url`` até receber 200, o processo terminar ou o prazo acabar."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return True
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            pass
        time.sleep(0.25)
    return False


def main() -> int:
    port = free_port()
    command = [sys.executable, "-m", "uvicorn", APP, "--factory"]
    command += ["--host", "127.0.0.1", "--port", str(port)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        ok = wait_for_ok(f"http://127.0.0.1:{port}/openapi.json", process, TIMEOUT_SECONDS)
    finally:
        process.terminate()
        try:
            output, _ = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            output, _ = process.communicate()
    if ok:
        print(f"Fumaça OK: /openapi.json respondeu 200 (uvicorn na porta {port}).")
        return 0
    reason = (
        f"o servidor terminou antes de responder (código {process.returncode})"
        if process.returncode not in (None, 0, -15)
        else f"sem 200 em /openapi.json em {TIMEOUT_SECONDS:.0f} s"
    )
    print(f"Fumaça falhou: {reason}.", file=sys.stderr)
    print(output, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

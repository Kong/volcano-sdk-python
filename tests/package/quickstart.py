"""Run the public quickstart with the interpreter's installed distribution."""

from __future__ import annotations

import io
import json
import os
import re
import runpy
import signal
import threading
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, NoReturn

if TYPE_CHECKING:
    from types import FrameType


def timeout(_signum: int, _frame: FrameType | None) -> NoReturn:
    message = "Documented quickstart timed out"
    raise TimeoutError(message)


def run_quickstart() -> None:
    document = (Path(__file__).resolve().parents[2] / "docs/README.md").read_text()
    section = document.split("## Sign in and read a profile\n")[1].split("\n## ")[0]
    examples = re.findall(r"```python\n([\s\S]*?)\n```", section)
    assert len(examples) == 1, "Expected one complete documented quickstart"
    user = {
        "id": "22222222-2222-4222-8222-222222222222",
        "project_id": "11111111-1111-4111-8111-111111111111",
        "email": "quickstart@example.test",
        "email_confirmed": True,
        "status": "active",
    }
    requests: list[tuple[str, str, str | None, Any]] = []

    class Handler(BaseHTTPRequestHandler):
        def _respond(self) -> None:
            raw = self.rfile.read(int(self.headers.get("Content-Length", "0")))
            body = json.loads(raw) if raw else None
            requests.append(
                (self.command, self.path, self.headers.get("Authorization"), body),
            )
            match (self.command, self.path):
                case ("POST", "/auth/signin"):
                    self._json(
                        {
                            "access_token": "synthetic-access",
                            "refresh_token": "synthetic-refresh",
                            "token_type": "bearer",
                            "expires_in": 3600,
                            "user": user,
                        },
                    )
                case ("GET", "/auth/user"):
                    self._json({"user": user})
                case ("POST", "/auth/logout"):
                    self.send_response(204)
                    self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()

        def _json(self, payload: Any) -> None:
            encoded = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_GET(self) -> None:
            self._respond()

        def do_POST(self) -> None:
            self._respond()

        def log_message(self, *_args: object, **_kwargs: object) -> None:
            pass

    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        previous_handler = signal.signal(signal.SIGALRM, timeout)
        try:
            signal.alarm(30)
            os.environ.update(
                VOLCANO_API_URL=f"http://127.0.0.1:{server.server_port}",
                VOLCANO_ANON_KEY="synthetic-anon",
                VOLCANO_USER_EMAIL=str(user["email"]),
                VOLCANO_USER_PASSWORD="synthetic-password",
            )
            output = io.StringIO()
            with TemporaryDirectory(prefix="volcano-quickstart-") as directory:
                example = Path(directory) / "quickstart.py"
                example.write_text(examples[0])
                with redirect_stdout(output):
                    runpy.run_path(str(example), run_name="__main__")
            assert output.getvalue().strip() == f"Signed in as {user['email']}"
            assert requests == [
                (
                    "POST",
                    "/auth/signin",
                    "Bearer synthetic-anon",
                    {"email": user["email"], "password": "synthetic-password"},
                ),
                ("GET", "/auth/user", "Bearer synthetic-access", None),
                (
                    "POST",
                    "/auth/logout",
                    "Bearer synthetic-anon",
                    {"refresh_token": "synthetic-refresh"},
                ),
            ]
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous_handler)
            server.shutdown()
            thread.join(timeout=5)


if __name__ == "__main__":
    run_quickstart()

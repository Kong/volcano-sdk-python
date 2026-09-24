---
title: Sandboxes
description: Run isolated commands and manage sessions, files, and HTTP services from Python.
---

Run a command from trusted backend code in an environment with Sandbox access enabled:

```python
import os
from uuid import uuid4
from volcano_sdk import VolcanoClient

client = VolcanoClient(
    anon_key=os.environ["VOLCANO_ANON_KEY"],
    service_key=os.environ["VOLCANO_SERVICE_KEY"],
    api_url=os.environ.get("VOLCANO_API_URL", "https://api.volcano.dev"),
)
project_id = os.environ["VOLCANO_PROJECT_ID"]
request_id = str(uuid4())
result = client.sandboxes.exec(
    project_id,
    'python -c "print(42)"',
    region="aws-us-east-1",
    preset="python3.12",
    request_id=request_id,
)
print(result.stdout, result.exit_code)
```

Keep the same `request_id` when retrying an uncertain create or execution. A new
ID represents a new operation. The SDK does not automatically replay commands.
Nonzero command exits and timeouts are result fields, not API exceptions.
API failures raise typed exceptions such as `ConflictError` or `RateLimitedError`;
these preserve `status`, `code`, and `retry_after` when supplied by the server.

## Keep a session

```python
import time

with client.sandboxes.create(
    project_id,
    region="aws-us-east-1",
    preset="python3.12",
    max_duration_seconds=300,
) as session:
    for _ in range(60):
        if session.refresh().state == "running":
            break
        time.sleep(1)
    else:
        raise TimeoutError("Sandbox did not become ready")
    session.files.write("/tmp/input.bin", bytes(range(256)))
    assert session.files.read("/tmp/input.bin") == bytes(range(256))
    result = session.exec("wc -c /tmp/input.bin")
    print(result.stdout)
```

Creation, suspension, resumption, and termination are asynchronous. Use `refresh()`
to observe state. Context exit requests termination even when the body raises;
it does not wait for termination to complete. Use `get(session_id)` to reconnect,
then `suspend()`, `resume()`, or `terminate()` as needed. File reads return `bytes`;
writes accept at most 8 MiB.

## Access a background HTTP service

Inside a running session, detach the service and redirect its streams:

```python
session.exec(
    "nohup python -m http.server 8080 --bind 0.0.0.0 >/tmp/http.log 2>&1 </dev/null &"
)
access = session.access(8080)
# Send access.token in X-Volcano-Sandbox-Token when requesting access.url.
```

The process lasts until it exits or its session ends. Access credentials are scoped
to the session and port and expire at `access.expires_at`. Do not log the token or
put it in URLs. See [Sandbox HTTP access](/platform/guides/sandboxes).

## Select presets and authorize users

`client.sandboxes.presets()` lists available presets and regions. Supply exactly
one of `preset` or a saved template's `sandbox_id`. Omit `memory_mb` to preserve
that template's configured memory.

Only trusted backend code should call
`client.sandboxes.grant(session_id, auth_user_id, expires_at)` or
`client.sandboxes.revoke(session_id, auth_user_id)`. Project users can access only
sessions explicitly granted to them; they cannot create or manage sessions.
Service keys stay on the backend. Anonymous keys alone cannot use this facade.

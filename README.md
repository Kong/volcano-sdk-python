# Volcano Python SDK

This private proof of concept validates Volcano's Python SDK contract. It is not
published to PyPI and is not ready for production use.

## Try the contract facade

The REST facade is synchronous. Create one client, sign in, and use the stored
session for database and storage requests. Configure a service key for locks.

```python
from volcano_sdk import VolcanoClient

client = VolcanoClient(
    api_url="https://api.volcano.dev",
    anon_key="your-anon-key",
    service_key="your-service-key",
)

session = client.auth.sign_in(email="user@example.com", password="secret")

rows = client.database("main").from_("items").select("*").eq("slug", "a").execute()

bucket = client.storage.from_("assets")
bucket.upload("a.txt", b"hello")
downloaded = bucket.download("a.txt")
assert downloaded == b"hello"

lease = client.locks.acquire("build", ttl=30)
client.locks.release("build", lease)
```

Realtime is async. Channels wrap `centrifuge-python`; the underlying client and
subscription objects are not part of the public API.

```python
channel = client.realtime.channel("updates")
channel.on("message", print)

await channel.subscribe()
await channel.send({"event": "message", "value": "contract"})
await channel.unsubscribe()
await client.realtime.disconnect()
```

## Compatibility

The POC supports Python 3.11 and 3.14. Its public facade is intentionally
independent of generated httpx types. Compatibility is verified against the
bundled Volcano API contract from hosting commit
`a3f4a6e9d0fb48a16621383bd796d8b0d1378630`; `openapi/openapi.yaml` has SHA-256
`c26ab2f32961699b19f710c1174906b7baae077eefcec299a6c19a36d2f559f6`.

The realtime wrapper includes a narrow compatibility adapter for Volcano's
project-prefixed publication channels. It still delegates connection,
subscription, publish, and disconnect behavior to `centrifuge-python` 0.6.

## Develop locally

```shell
uv sync --frozen
uv run python scripts/check_openapi.py
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pyright
uv run pytest tests/unit -q
uv run python -m build
```

Live contract scenarios require an isolated fixture produced by
`volcano-hosting/tests/sdk-contract/support/fixture.mjs`:

```shell
VOLCANO_SDK_CONTRACT_FIXTURE=/absolute/path/to/fixture.json \
  uv run behave features/contract --junit --junit-directory reports/behave
```

The fixture must be an absolute path to a mode-`0600` JSON file.

See [Authentication](docs/authentication.md) for account, session, hosted auth,
and OAuth examples.

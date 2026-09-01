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

sign_up = client.auth.sign_up(
    email="new-user@example.com",
    password="secret",
    metadata={"display_name": "New User"},
)
if sign_up.confirmation_required:
    print(sign_up.message)

session = client.auth.sign_in(email="user@example.com", password="secret")
current_session = client.auth.get_session()
assert current_session == session

user = client.auth.get_user()
assert user.id == session.user_id

updated_user = client.auth.update_user(
    password="new-secret",
    metadata={"display_name": "Grace", "avatar": None},
)
assert updated_user.id == session.user_id

rows = client.database("main").from_("items").select("*").eq("slug", "a").execute()

bucket = client.storage.from_("assets")
bucket.upload("a.txt", b"hello")
downloaded = bucket.download("a.txt")
assert downloaded == b"hello"

lease = client.locks.acquire("build", ttl=30)
client.locks.release("build", lease)
```

`sign_up()` returns an immutable acknowledgement and never creates or replaces a session. The
response is identical for new and existing email addresses. Call `sign_in()` separately after the
account is ready to establish a session.

`get_session()` reads immutable local state. It does not refresh or validate the token.

`get_user()` sends the active access token to Volcano and returns an immutable, server-validated
profile with the complete public AuthUser fields. Profile timestamps are timezone-aware `datetime`
values, and nested user and application metadata are immutable. The request does not replace the
session or cache the profile. If another authentication operation replaces the session while the
request is in flight, `get_user()` raises `SessionChangedError` instead of returning a profile for
stale credentials.

`update_user()` updates the current user's password, metadata, or both. Metadata is a shallow patch:
omitted keys remain unchanged, and setting a key to `None` removes it. The method returns the same
immutable profile type as `get_user()` and does not replace the active session. It also rejects a
response if another authentication operation replaces the session while the update is in flight.

Request a password reset email without creating or changing a session:

```python
client.auth.reset_password_for_email(email="user@example.com")
```

When transactional email is configured, Volcano sends the reset link. Success returns `None`, and
the response is intentionally identical whether or not the email belongs to an account. Failures
raise the same typed Volcano errors as other authentication operations.

Confirm an email address with the token from its confirmation link:

```python
client.auth.confirm_email(token="confirmation-token")
```

Success returns `None`. Confirmation does not sign in the confirmed account or change an unrelated
local session.

Request another confirmation email without revealing account state:

```python
client.auth.resend_confirmation(email="user@example.com")
```

Success returns `None` whether the account is unknown, already confirmed, or eligible. Volcano sends
mail only for an existing unconfirmed account when transactional email is configured. Rate limits
raise `RateLimitedError` with `retry_after` when the server supplies it.

Request confirmation for a new email address while keeping the current session:

```python
result = client.auth.request_email_change(new_email="new@example.com")
print(result.new_email)
```

The immutable result contains the server acknowledgement. Its `message` and `new_email` fields may
be `None`. The request fails if there is no active session or that session changes in flight.

Create an anonymous account and make its tokens the current session:

```python
session = client.auth.sign_in_anonymously(metadata={"device": "mobile"})
```

Anonymous sign-ins must be enabled for the project. Convert the account before signing out if the
user needs to recover it later.

Attach email credentials without changing the anonymous user's ID or current session:

```python
user = client.auth.convert_anonymous(
    email="user@example.com",
    password="secure-password",
    metadata={"display_name": "Ada"},
)
```

When email confirmation is required, confirm the new address before treating it as verified.

Set a new password with the recovery token from that email:

```python
client.auth.reset_password(
    token="recovery-token",
    new_password="new-secret",
)
```

Success returns `None`. The reset revokes the recovered account's existing sessions and does not
sign it in. The client keeps any unrelated local session unchanged; sign in with the new password
when the reset flow completes.

Copy a complete native session into another client's memory:

```python
session = source.auth.get_session()
if session is not None:
    fresh.auth.set_session(session)
```

`set_session()` copies the session without making a request or persisting credentials. It raises
`ValueError` when the session type or any credential field is incomplete.

Refresh the session with its current refresh token:

```python
refreshed = client.auth.refresh_session()
assert client.auth.get_session() is refreshed
```

On success, `refresh_session()` replaces the in-memory session and returns the immutable new
snapshot. An authentication failure clears the session that initiated the request. Server and
transport failures preserve it, and a late response never replaces a newer session. The SDK does
not persist sessions.

Sign out by revoking and clearing the current session:

```python
client.auth.sign_out()
assert client.auth.get_session() is None
```

Calling `sign_out()` without a session succeeds without a request. A revocation failure is raised
after the captured local session is cleared. A newer session established while sign-out is in
flight remains current.

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

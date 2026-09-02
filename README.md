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
first_kibibyte = bucket.download("archive.bin", byte_range="bytes=0-1023")
upload_session = bucket.create_upload_session(
    "videos/demo.mp4",
    total_size=20_000_000,
    content_type="video/mp4",
    part_size=8_388_608,
)
print(upload_session.session_id, upload_session.total_parts)
part = bucket.upload_part(
    "videos/demo.mp4",
    session_id=upload_session.session_id,
    part_number=1,
    data=b"x" * upload_session.part_size,
)
print(part.etag)

page = bucket.list("avatars", limit=100)
for object_ in page.objects:
    print(object_.name)

if page.next_cursor is not None:
    next_page = bucket.list("avatars", limit=100, cursor=page.next_cursor)

removed_paths = bucket.remove(["archive/a.txt", "archive/b.txt"])
moved = bucket.move("drafts/a.txt", "published/a.txt")
copied = bucket.copy("templates/a.txt", "drafts/a.txt")
public_object = bucket.update_visibility("avatars/a.png", is_public=True)
print(public_object.public_url)
public_url = bucket.get_public_url("avatars/a.png")
print(public_url)

lease = client.locks.acquire("build", ttl=30)
client.locks.release("build", lease)
```

Storage removals run in input order. A failed request raises after any earlier
paths have already been deleted. Visibility updates return the server-confirmed
object; `public_url` is set only when the object is public.
`get_public_url()` constructs a URL locally and does not check object visibility.
Pass an HTTP byte range to download only part of an object.
`create_upload_session()` returns the immutable server-selected part size,
part count, and expiration time for a resumable upload.
`upload_part()` returns immutable part metadata and can safely retry the same
part number to replace that part.

Database builders are immutable, so you can safely reuse a base query. Chain `neq()`, `gt()`,
`gte()`, `lt()`, and `lte()` for comparison filters:

```python
base_query = client.database("main").from_("items").select("id", "priority")
rows = (
    base_query.gte("priority", 3)
    .lt("priority", 10)
    .order("priority", ascending=False)
    .order("id")
    .limit(10)
    .offset(20)
    .execute()
)

matching_rows = (
    client.database("main")
    .from_("items")
    .select("*")
    .ilike("name", "%volcano%")
    .is_("deleted_at", None)
    .in_("status", ["draft", "published"])
    .execute()
)

inserted_rows = (
    client.database("main")
    .from_("items")
    .insert({"name": "Volcano", "status": "draft"})
    .execute()
)

updated_rows = (
    client.database("main")
    .from_("items")
    .update({"status": "published"})
    .eq("name", "Volcano")
    .execute()
)

deleted_rows = (
    client.database("main").from_("items").delete().eq("name", "Volcano").execute()
)
```

Updates and deletes require at least one filter; Volcano rejects filterless mutations.

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

Cancel the pending change while keeping the current session:

```python
client.auth.cancel_email_change()
```

Success returns `None`. A successful stale response is rejected if another authentication operation
replaces the session while cancellation is in flight.

Confirm the pending change with the token delivered to the new address:

```python
user = client.auth.confirm_email_change(token="email-change-token")
print(user.email)
```

The method returns the immutable updated user without replacing the active session. A successful
stale response is rejected if another authentication operation replaces that session in flight.

List sessions using the stable activity-ordered offset pagination:

```python
page = client.auth.list_sessions(page=1, limit=20)
for session in page.sessions:
    print(session.id, session.user_agent, session.is_current)
```

The method returns immutable `SessionPage` and `AuthSession` values. It raises
`SessionChangedError` instead of returning a page for a session that was replaced while the request
was in flight. Sort, filter, and cursor controls are not yet exposed by this facade.

Build a managed hosted-auth URL:

```python
import secrets

hosted_state = secrets.token_urlsafe(32)
hosted_url = client.auth.get_hosted_auth_url(
    project_id="00000000-0000-4000-8000-000000000020",
    action="signup",
    state=hosted_state,
)
```

Store `hosted_state` in the user's signed server-side session before redirecting to `hosted_url`.
After parsing the returned fragment into a `Session`, validate and adopt it atomically:

```python
session = client.auth.adopt_hosted_auth_session(
    returned_session,
    state=returned_state,
    expected_state=hosted_state,
)
```

The SDK rejects a mismatched state before changing local authentication. It builds and adopts the
flow but does not parse browser URLs, navigate, or persist state. The `action` deep link applies to
Volcano's built-in page; a customized login page must implement its own signup or forgot-password
flow.

Build the URL that starts an OAuth sign-in flow:

```python
import secrets

oauth_state = secrets.token_urlsafe(32)
authorization_url = client.auth.sign_in_with_oauth(
    provider="github",
    redirect_to="https://app.example.com/auth/callback",
    state=oauth_state,
)
```

Store `oauth_state` in the user's signed server-side session, then redirect the user to the returned
URL. In the callback, pass the returned and stored states to the SDK so it rejects login CSRF before
exchanging the one-time code:

```python
session = client.auth.exchange_oauth_code(
    code=callback_code,
    redirect_to="https://app.example.com/auth/callback",
    state=callback_state,
    expected_state=stored_oauth_state,
)
```

The callback URL must exactly match a registered project redirect. The exchange stores the returned
Volcano session on the client. The SDK does not open a browser or persist OAuth state between
requests; use your framework's signed session or equivalent storage for that state.

List the OAuth providers linked to the current account:

```python
providers = client.auth.list_linked_oauth_providers()
for provider in providers:
    print(provider.provider, provider.linked_at)
```

The method returns an immutable tuple of `LinkedOAuthProvider` values and raises
`SessionChangedError` if the active session changes while the request is in flight.

Start linking another OAuth provider to the current account:

```python
authorization_url = client.auth.link_oauth_provider(provider="github")
```

Redirect the user to the returned URL to complete the provider flow. The method accepts `apple`,
`github`, `google`, or `microsoft` and raises `SessionChangedError` if the active session changes
while the request is in flight.

Unlink an OAuth provider from the current account:

```python
client.auth.unlink_oauth_provider(provider="github")
```

The server rejects removal of the account's only authentication method. A successful stale response
raises `SessionChangedError` instead of acknowledging work authorized by a replaced session.

Check whether Volcano has a valid server-held provider token:

```python
status = client.auth.get_oauth_provider_token(provider="github")
print(status.provider, status.expires_in)
```

The immutable `OAuthProviderTokenStatus` contains provider and expiry metadata, not the credential.
Volcano refreshes an expired token on the server. A stale result raises `SessionChangedError`.

Refresh a provider token explicitly:

```python
status = client.auth.refresh_oauth_provider_token(provider="github")
print(status.provider, status.expires_in)
```

The refresh credential and new access token remain on the server. A stale result raises
`SessionChangedError`.

Call a provider API through Volcano's fixed-host server proxy:

```python
repos = client.auth.call_oauth_api(
    provider="github",
    endpoint="/user/repos",
)
print(repos[0]["name"])
```

The method returns an immutable copy of the provider's JSON value. Volcano owns token refresh and
host validation. A stale result raises `SessionChangedError`.

Sign out every other device while keeping the current session active:

```python
client.auth.delete_all_other_sessions()
```

Success returns `None`. Do not replace the client's session while this request is in flight: the
server may revoke that replacement as an "other" session. If replacement occurs, the method raises
`SessionChangedError` instead of acknowledging a stale result.

Revoke one session by ID:

```python
client.auth.delete_session(session_id="00000000-0000-4000-8000-000000000099")
```

The request uses the current access token. Deleting that token's own session clears local
credentials, including when the request outcome is uncertain; deleting another session preserves
them. If another authentication operation replaces the session before deletion finishes, the method
raises `SessionChangedError` instead of clearing the replacement or acknowledging a stale result.

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

Observe local session transitions:

```python
from volcano_sdk import AuthChangeEvent, Session


def handle_auth_change(event: AuthChangeEvent, session: Session | None) -> None:
    print(event, session is not None)


subscription = client.auth.on_auth_state_change(handle_auth_change)
# Later, stop receiving events.
subscription.unsubscribe()
```

Registration queues `INITIAL_SESSION`. It normally arrives before registration returns, but an
existing notification dispatch may deliver it afterward. Successful session creation, refresh, and
local clearing emit `SIGNED_IN`, `TOKEN_REFRESHED`, and `SIGNED_OUT`. Callbacks are delivered locally
in transition order after the state lock is released, and callback failures cannot interrupt auth
operations. Unsubscribing prevents queued and future delivery; a callback already selected for
delivery may finish after `unsubscribe()` returns. The SDK does not broadcast between processes or
persist sessions.

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
`cb12eb4636252cb658f13850dad930fa73a5dc4c`; `openapi/openapi.yaml` has SHA-256
`95e5c102830db382064180afca4c62ad8b11faabf58148f9d21236046b930090`.

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

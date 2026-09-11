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

function = client.functions.invoke(
    "send-welcome",
    {"user_id": session.user_id},
)
print(function.status, function.version, function.data)

logs = client.logs.search(
    "00000000-0000-4000-8000-000000000001",
    {"resource": {"type": "function"}, "limit": 100},
)
for event in logs.data:
    print(event["timestamp"], event["body"])

activity = client.logs.activity(
    "00000000-0000-4000-8000-000000000001",
    {"resource": {"type": "function"}, "bucket_count": 24},
)
print(activity.total)

rows = client.database("main").from_("items").select("*").eq("slug", "a").execute()

bucket = client.storage.from_("assets")
bucket.upload("a.txt", b"hello", content_type="text/plain; charset=utf-8")
with open("avatar.png", "rb") as avatar:
    bucket.upload("avatars/me.png", avatar)
downloaded = bucket.download("a.txt")
assert downloaded == b"hello"
first_kibibyte = bucket.download("archive.bin", byte_range="bytes=0-1023")
video = b"demo video"
uploaded = bucket.upload_resumable(
    "videos/automatic.mp4",
    video,
    content_type="video/mp4",
    on_progress=lambda uploaded, total: print(f"{uploaded}/{total}"),
)
print(uploaded.name)
upload_session = bucket.create_upload_session(
    "videos/demo.mp4",
    total_size=len(video),
    content_type="video/mp4",
    part_size=8_388_608,
)
print(upload_session.session_id, upload_session.total_parts)
part = bucket.upload_part(
    "videos/demo.mp4",
    session_id=upload_session.session_id,
    part_number=1,
    data=video,
)
print(part.etag)
status = bucket.get_upload_session(
    "videos/demo.mp4",
    session_id=upload_session.session_id,
)
print(status.parts_uploaded, status.bytes_uploaded)
completed = bucket.complete_upload_session(
    "videos/demo.mp4",
    session_id=upload_session.session_id,
)
print(completed.name)

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

state = client.locks.get("build")
print(state.held)
lease = client.locks.acquire("build", ttl=30)
lease = client.locks.renew("build", lease, ttl=30)
client.locks.release("build", lease)
client.locks.force_release("stale-build")

with client.locks.with_lock("deploy", ttl=30) as guard:
    print(guard.lease.fencing_token)
```

Function invocation returns `data=None` for an empty HTTP 204 response, retaining
the status, headers, and version.

Simple uploads accept an optional `content_type` for the multipart file part.
Omit it or pass `None` to retain `application/octet-stream`. Explicit values must
be non-blank printable ASCII; MIME parameters such as `charset=utf-8` are allowed.

Storage removals run in input order. A failed request raises after any earlier
paths have already been deleted. Visibility updates return the server-confirmed
object; `public_url` is set only when the object is public.
`get_public_url()` constructs a URL locally and does not check object visibility.
Pass an HTTP byte range to download only part of an object.
`create_upload_session()` returns the immutable server-selected part size,
part count, and expiration time for a resumable upload.
`upload_resumable()` accepts bytes or a binary file-like object, creates a
session, and uploads server-sized chunks. It streams seekable files directly;
non-seekable inputs are spooled to a temporary file with bounded reads. If a
part or progress callback fails, it makes a best-effort abort and raises the
original error. `on_progress` runs after each successful part with cumulative
uploaded bytes and the total size.
`upload_part()` returns immutable part metadata and can safely retry the same
part number to replace that part.
`locks.get()` returns immutable lock availability, expiry, and fencing-token
state without acquiring the lock.
Lock acquisition and renewal require an integer TTL from 5 seconds through 90 days.
`locks.renew()` returns a new immutable lease and leaves the previous value
unchanged.
`locks.with_lock()` renews the lease on a background thread, stops renewal
before releasing the latest lease, and yields a `LockGuard`. Read
`guard.lease` for the latest fencing token. Check `guard.lost` or call
`guard.wait_lost(timeout=...)` when work must stop promptly after ownership is
lost. If the context body succeeds, a renewal failure is raised after release;
an exception from the body takes precedence.
`locks.force_release()` drops any current lease without an ownership token.
Use it only for administrative recovery behind fencing-token enforcement.
`get_upload_session()` returns immutable progress and uploaded-part metadata for
resuming an interrupted upload.
`complete_upload_session()` assembles the uploaded parts and returns the stored
object.
`abort_upload_session(path, session_id=...)` abandons a session and discards its
uploaded parts.

`functions.invoke()` resolves a DNS-safe function name and sends a JSON object.
It uses the active user session when present, then a configured service key,
then the anonymous key. An anonymous key can invoke a public function without a
user session; the function receives no user identity. The immutable result
includes the response body, status, headers, and `X-Volcano-Version`. The body
can be a JSON object, array, scalar, or text; an empty body returns `None`.
JSON arrays become immutable tuples. Invalid JSON is returned as text. A
function's own non-2xx response is returned when the version header proves it
ran; platform failures raise typed SDK errors.

`logs.search()` returns an immutable page of retained runtime or deployment log
events. Pass `next_cursor` back as `cursor` to continue a search. `logs.activity()`
returns immutable time buckets using the same resource selector and query syntax.
Both methods require an active user session.

Database selects, inserts, updates, deletes, and log reads refresh the captured
session after an HTTP 401 and retry the same request once. Concurrent requests reuse a successful
refresh for that session.
Replacing or signing out the session before replay, or while replay is in flight,
raises `SessionChangedError`. Requests do not wait for auth callbacks running on
another thread. A later callback-driven session change does not invalidate a
completed request.
A failed refresh preserves the original request error. HTTP 403 responses and
network failures do not trigger this retry. Mutations are replayed only after an
explicit authentication rejection, never after an ambiguous transport failure.

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

Use `database_connection_string()` inside a Volcano function to select database
access without changing the advertised `DATABASE_URL` target:

```python
import os

from volcano_sdk import database_connection_string

connection_string = database_connection_string(
    os.environ["DATABASE_URL"],
    user_id=event.get("__volcano_auth", {}).get("user_id"),
)
```

Pass a user ID to enforce that user's Row-Level Security policies. Omit
`user_id` for full service access.
The helper preserves libpq connection syntax, including hostless and multi-host
targets, and leaves unrelated query values unchanged.

`sign_up()` returns an immutable acknowledgement without changing the session by default.
The signup acknowledgement is identical for new and existing email addresses. Pass
`sign_in_when_allowed=True` to follow it with `sign_in()` only when confirmation is not required:

```python
result = client.auth.sign_up(
    email="new-user@example.com", password="secret", sign_in_when_allowed=True
)
session = result.session  # None when no follow-up sign-in ran.
```

A successful follow-up stores the session and emits the normal sign-in event. A failed
follow-up raises its usual typed error; it does not undo the successful signup.

`get_session()` reads immutable local state. It does not refresh or validate the token.

Sessions returned by authentication retain the user payload in `session.user`,
including metadata. The snapshot is deeply immutable and available without a
request. It is cached data, not proof of authentication; use `auth.get_user()`
to fetch the server-validated profile. Existing three-field `Session` construction
still works, with `user=None`. An adopted snapshot must have the same user ID.
Successful `get_user()`, `update_user()`, `convert_anonymous()`, and
`confirm_email_change()` calls update that local snapshot without changing tokens
or emitting an auth-state event. Previously returned sessions remain immutable.

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

`set_session()` copies the session without making a request, persisting credentials, or notifying
auth-state subscribers. It raises `ValueError` when the session type or any credential field is
incomplete.

Password sign-in raises `SessionChangedError` if local session state changes while the request is
in flight. The late response does not replace the newer state or emit a sign-in notification.

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
stop_connect = client.realtime.on_connect(
    lambda context: print("connected", context.client)
)
client.realtime.on_disconnect(
    lambda context: print("disconnected", context.code, context.reason)
)
client.realtime.on_error(
    lambda context: print("realtime error", context.code, context.message)
)

channel = client.realtime.channel("updates")
assert channel.name == "broadcast:updates"
channel.on("message", print)

await channel.subscribe()
assert client.realtime.is_connected
await channel.send({"event": "message", "value": "contract"})
await client.realtime.remove_channel("updates")
assert client.realtime.is_connected
await client.realtime.disconnect()
assert not client.realtime.is_connected
stop_connect()
```

Broadcast channels use Centrifuge's native stream recovery when server history
is available. `await channel.unsubscribe()` pauses delivery while retaining the
in-memory recovery position; a later `await channel.subscribe()` resumes the
same subscription and requests missed publications. Removing the channel or
disconnecting the realtime client discards that position. Recovery is not
persisted across processes and never crosses an auth session lineage.

Presence channels expose server-managed user metadata and join/leave events:

```python
presence = client.realtime.channel("lobby", channel_type="presence")
presence.on("join", lambda info: print("joined", info.user, info.data))
presence.on("leave", lambda info: print("left", info.user))
stop_sync = presence.on_presence_sync(
    lambda state: print("present clients", tuple(state))
)

await presence.subscribe()
await presence.track({"status": "online"})
assert presence.tracked_state == {"status": "online"}
current = presence.get_presence_state()
await client.realtime.remove_channel("lobby", channel_type="presence")
stop_sync()
```

`remove_channel()` unsubscribes and forgets one channel. `remove_all_channels()`
does the same for every managed channel without disconnecting the shared
realtime transport, so later calls to `channel()` return fresh facades.
Connection callbacks receive immutable contexts, may be synchronous or async,
and run outside the transport event processor. Each registration returns an
idempotent function that stops future delivery.
Access-token refreshes preserve a realtime connection only while the auth
session lineage remains current. After signing in again or changing users,
call `disconnect()` before subscribing channels for the new session; the SDK
refuses to rebind an existing connection across that identity boundary.
Presence state and client metadata are immutable snapshots. Volcano derives
the remote identity and metadata from the authenticated user; `track()` stores
optional local state in `tracked_state` but does not replace that server-managed
identity. Presence is resynchronized after reconnects. Query failures are
reported through `realtime.on_error()` and clear the current snapshot.

Postgres channels deliver immutable, RLS-scoped row changes and filter
callbacks by event, schema, and table:

```python
client.realtime.set_database_name("app")
changes = client.realtime.channel(
    "public:messages",
    channel_type="postgres",
    auto_fetch=True,
    fetch_batch_window_ms=20,
    fetch_max_batch_size=50,
)
stop_changes = changes.on_postgres_changes(
    "INSERT",
    schema="public",
    table="messages",
    callback=lambda change: print(change.record),
)
await changes.subscribe()
stop_changes()
```

Binding a database automatically fetches the matching row for lightweight
`INSERT` and `UPDATE` notifications in the `public` schema. The fetch uses the
realtime connection's RLS-scoped access token. Compatible row lookups are
batched while callback delivery preserves publication order.
If the row is absent or the query fails, the callback receives the lightweight
notification with its `id` and `mode` intact. Non-public schemas also retain
that lightweight form. Lightweight deletes never query the database; they
preserve `old_record`, or provide `{"id": change.id}` when no old row was
included. Tune a channel's batching with `fetch_batch_window_ms` and
`fetch_max_batch_size`; the defaults are 20 milliseconds and 50 rows. Set
`auto_fetch=False` on a Postgres channel to keep lightweight notifications
without querying their rows. Pass `None` to `set_database_name()` to disable
row fetching for every channel.

## Compatibility

The POC supports Python 3.11 and 3.14. Its public facade is intentionally
independent of generated httpx types. The bundled `openapi/openapi.yaml` matches
the public bundle from [Hosting #991](https://github.com/Kong/volcano-hosting/pull/991)
at commit `ef03f689e`.
Its SHA-256 is `076d97809c95f50567d8b100f4188c1fe2b74e73a388e335c79850e66edfc0e4`.

Generated operations are internal. Transport adapters use `sync_detailed()` or
`asyncio_detailed()` to inspect HTTP status before interpreting the parsed body.
The generated parsed-body-only shortcuts are not public SDK APIs.

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

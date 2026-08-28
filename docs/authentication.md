# Authentication

Create a client with your project URL and anonymous key, then use `client.auth`
for account and session operations.

```python
from volcano_sdk import VolcanoClient

client = VolcanoClient(
    api_url="https://api.volcano.dev",
    anon_key="your-anon-key",
)

session = client.auth.sign_in(
    email="user@example.com",
    password="your-password",
)

print(client.current_user.id)
print(session.expires_in)
```

The client keeps the active `current_user` and `current_session` in memory.
Pass both tokens when restoring an existing session in a new client. An access
token without a refresh token is valid, but a refresh token without an access
token is rejected.

```python
restored = VolcanoClient(
    api_url="https://api.volcano.dev",
    anon_key="your-anon-key",
    access_token=session.access_token,
    refresh_token=session.refresh_token,
)

restored.auth.refresh_session()
```

Store tokens in the secure storage provided by your runtime. Do not log them or
place them in source control.

## Manage the session

Subscribe to auth-state changes when application state must follow the client.
The listener runs immediately when the client is signed out or already has a
resolved user, then after committed auth changes. For restored tokens without a
loaded profile, the first event waits for `get_user()` or `refresh_session()` so
the client does not report a valid session as signed out. Call the returned
function to unsubscribe.

```python
unsubscribe = client.auth.on_auth_state_change(
    lambda user: print("signed in" if user else "signed out")
)

client.auth.refresh_session()
client.auth.sign_out()
unsubscribe()
```

A failed refresh clears local authentication so stale credentials are not
reused. `sign_out()` also clears local state if the remote revoke fails.

List and revoke device sessions through the same facade:

```python
page = client.auth.get_sessions(sort="created_at", status="active", limit=20)

for device_session in page.sessions:
    print(device_session.id, device_session.last_activity_at)

if page.next_cursor:
    cursor_page = client.auth.get_sessions(
        sort="created_at",
        status="active",
        cursor=page.next_cursor,
        limit=20,
    )

client.auth.delete_session(session_id="session-id")
client.auth.delete_all_other_sessions()
```

## Use password policy and device authorization

Read the server-enforced policy instead of duplicating password rules:

```python
policy = client.auth.get_password_policy()
print(policy.effective_min_length, policy.compromised_passwords_rejected)
```

An RFC 8628 device client starts authorization and polls at the returned
interval. A successful poll commits the returned user and session to that
client. The signed-in verifier approves the code on a separate client:

```python
authorization = device_client.auth.start_device_authorization(client_id="volcano-cli")
print(authorization.verification_uri, authorization.user_code)

verifier.auth.verify_device(user_code=authorization.user_code, action="approve")
session = device_client.auth.poll_device_token(
    client_id="volcano-cli",
    device_code=authorization.device_code,
)
```

After the device client commits its approved device-flow session, it can
exchange that verified session for a short-lived platform token. Ordinary
email/password and OAuth sessions are not eligible. Treat `token.token` as a
secret:

```python
token = device_client.auth.exchange_platform_token(client_id="volcano-cli")
```

## Create and update accounts

Sign-up can return without a session when email confirmation is required.

```python
result = client.auth.sign_up(
    email="new-user@example.com",
    password="your-password",
    user_metadata={"plan": "starter"},
)

if result.confirmation_required:
    print("Check your email")
```

Update the current user, or start with an anonymous account and preserve its
identity when converting it:

```python
client.auth.update_user(user_metadata={"plan": "pro"})

client.auth.sign_out()
client.auth.sign_up_anonymous(user_metadata={"source": "demo"})
anonymous_id = client.current_user.id

converted = client.auth.convert_anonymous(
    email="converted@example.com",
    password="your-password",
)
assert converted.id == anonymous_id
```

Conversion is permanent once the API accepts it. If the follow-up token rotation
fails, the method still returns the converted user and clears the local session;
sign in with the new credentials to continue.

Email workflows are available as explicit operations:

```python
client.auth.resend_confirmation(email="new-user@example.com")
client.auth.confirm_email(token="confirmation-token")
client.auth.forgot_password(email="user@example.com")
client.auth.reset_password(
    token="recovery-token",
    new_password="your-new-password",
)

change = client.auth.request_email_change(new_email="next@example.com")
client.auth.confirm_email_change(token="email-change-token")
# Or cancel a pending request:
client.auth.cancel_email_change()
```

Password reset revokes the reset account's existing sessions. If this client is
using one of them, `reset_password()` clears it before returning; sign in with
the new password to continue.

## Open hosted auth and OAuth

Hosted auth returns a URL and generated state value for your application to
retain before navigation:

```python
request = client.auth.get_hosted_auth_url(
    project_id="project-id",
    action="login",
)
print(request.authorization_url)
```

When hosted auth redirects back, compare the returned state with
`request.state` before adopting any returned credentials. The Python SDK does
not consume browser callbacks automatically.

OAuth authorization follows the same pattern. Preserve `request.state` and
pass it as `expected_state` during exchange; the SDK rejects a mismatch before
calling the API.

```python
request = client.auth.get_oauth_authorization_url(
    provider="github",
    redirect_url="https://app.example.com/auth/callback",
)

# After the provider redirects to your application:
client.auth.exchange_oauth_code(
    code="authorization-code",
    redirect_url="https://app.example.com/auth/callback",
    state="state-from-callback",
    expected_state=request.state,
)
```

Signed-in users can link providers, inspect them, refresh provider tokens, and
call provider APIs through Volcano:

```python
link = client.auth.link_oauth_provider(
    provider="github",
    redirect_url="https://app.example.com/auth/link/callback",
)

providers = client.auth.get_linked_oauth_providers()
token = client.auth.get_oauth_provider_token(provider="github")
client.auth.refresh_oauth_token(provider="github")
profile = client.auth.call_oauth_api(
    provider="github",
    endpoint="/user",
)
client.auth.unlink_oauth_provider(provider="github")
```

## Manage identities and sign-in methods

List the email identities and sign-in methods owned by the current account:

```python
identities = client.auth.list_identities()
methods = client.auth.list_methods()

for identity in identities:
    print(identity.email, identity.is_primary)

for method in methods:
    print(method.type, method.provider, method.is_primary)
```

Promote a sign-in method or unlink a non-primary identity by its ID:

```python
promoted = client.auth.promote_method(method_id="method-uuid")
client.auth.unlink_identity(identity_id="identity-uuid")
```

The API refuses to unlink a primary or last identity, or an identity whose
removal would leave the account without a sign-in method.

Keep generated state values and provider tokens secret. Navigate to the returned
authorization URL only after storing its matching state value.

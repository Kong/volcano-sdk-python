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
print(session.expires_at)
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
The listener runs immediately with the current user and after committed auth
changes. Call the returned function to unsubscribe.

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
page = client.auth.get_sessions(page=1, limit=20)

for device_session in page.sessions:
    print(device_session.id, device_session.last_seen_at)

client.auth.delete_session(session_id="session-id")
client.auth.delete_all_other_sessions()
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

Keep generated state values and provider tokens secret. Navigate to the returned
authorization URL only after storing its matching state value.

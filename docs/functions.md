---
title: Functions
description: Invoke deployed Volcano functions from Python and inspect their response status, headers, and data.
order: 5
---

Invoke a deployed function by its name.
This example assumes a public function named `hello` that accepts a JSON object.

```python
import os

from volcano_sdk import VolcanoClient

client = VolcanoClient(
    anon_key=os.environ["VOLCANO_ANON_KEY"],
    api_url=os.environ.get("VOLCANO_API_URL", "https://api.volcano.dev"),
)
result = client.functions.invoke("hello", {"name": "Ada"})
print(result.status)
print(result.data)
print(result.version)
```

The SDK resolves the function's invocation endpoint and caches it for the lifetime provided by Volcano.
Allow outbound requests to the resolved function domain as well as the API host.
Deployments without a separate function domain use the API invocation endpoint.

## Choose the invocation identity

The SDK uses the current user's access token when a session exists, otherwise a configured service key, otherwise the anonymous key.
Use the [quickstart](./README.md) to sign in before invoking a function that requires a user.
An invocation authorized only by the anonymous key has no user identity.

Supply `service_key` to the client constructor for trusted server operations that require it.
Use a separate client for each independent user session.

## Read the result

`FunctionResponse` is immutable and exposes `status`, `headers`, `version`, and `data`.
The payload sent to `invoke()` must be a JSON object; omitting it sends an empty object.
Response data can be a JSON object, array, scalar, text, or `None` for an empty body.
JSON arrays become immutable tuples, and invalid JSON is returned as text.

A function's own non-success response is returned as a result when Volcano confirms the function ran.
Check `result.status` to handle those application errors.
Failures before dispatch raise typed SDK exceptions such as `NotFoundError` or `AuthenticationError`.

If a cached function identity no longer exists, the SDK resolves the name again and retries once only when the platform confirms no function was dispatched.
A function's own HTTP 404 does not trigger another invocation.
Network failures do not establish whether a function ran; do not blindly retry operations with side effects.

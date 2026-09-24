# Typed authentication boundaries

Keep the existing public Auth methods while giving sibling facades an explicit,
typed request interface. `AuthRequests` owns refresh, replay, revocation, and
session ownership. One instance is shared by the client and authentication facade;
its state is never copied during a request. Email and OAuth mixins group public
operations by responsibility. Response validation and client capabilities live in
private modules with normal internal names.

The public 31-method Auth parameter lists are unchanged. `Auth(client)` remains
valid; a keyword-only `_requests` argument lets the client inject its shared
coordinator. No internal lifecycle method is added to the public facade. Existing
concurrency, credential-scoping, package typing, and full-coverage tests check this
boundary.

Research checked on 2026-09-24:

- **Adopt:** [Stripe](https://github.com/stripe/stripe-python/blob/master/stripe/_stripe_client.py)
  creates one request coordinator and injects it into resource services.
- **Adapt:** [HTTPX](https://github.com/encode/httpx/blob/master/httpx/_client.py)
  uses a common typed client base and optional transport injection. Our shared
  base only provides authentication capabilities to the operation groups.
- **Reject:** [Supabase Auth](https://github.com/supabase/auth-py/blob/main/supabase_auth/_sync/gotrue_client.py)
  demonstrates dependency injection but also dynamically binds some service
  methods. Static classes and explicit signatures keep our all-mode type checks
  effective.

The optional internal injection preserves standalone construction while avoiding
callback rebinding or public forwarding methods for private operations.

The same static grouping keeps `GeneratedTransport` operations in six modules:
authentication, account management, database, storage, execution, and locks. They
share one typed HTTP configuration base; response normalization is independent of
the operation groups. All 57 operation parameter lists remain unchanged.

Public facade constructors also accept a `VolcanoClient` directly. Two typed
adapters obtain its private authentication or facade context; this preserves the
existing constructors without publishing internal client methods. Dataclass
builders retain their parameter names and defaults and resolve the context before
an operation. Each adapter's exact private factory call has documented Ruff and
Basedpyright exceptions, checked against its literal call and function scope.

The context protocols describe private client wiring. They are not root-package
exports or documented consumer extension points; direct construction tests use
`VolcanoClient` and the documented public facade methods.

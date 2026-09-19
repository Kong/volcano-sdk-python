# Realtime compatibility exception

The Python SDK temporarily adapts the official client's subscription lookup to
Volcano's project-prefixed wire channels. Removal is tracked in
[VOL-1054](https://konghq.atlassian.net/browse/VOL-1054). This is the bounded interim
policy allowed by [VOL-947](https://konghq.atlassian.net/browse/VOL-947); the adapter
has not been removed.

## Dependency and scope

`pyproject.toml` allows `centrifuge-python>=0.6.0,<0.7.0`. The current `uv.lock`
resolves 0.6.0. Keep the upper bound until a reviewed replacement is available.
Do not assume other patch versions have passed the recorded acceptance run.

`_VolcanoCentrifugeConnection` replaces the official client's private `_subs`
dictionary with `_ProjectAwareSubscriptions`. It maps incoming prefixed channel
names and user-scoped Postgres routes to the SDK's local subscription. Connection,
subscription, recovery, publication, presence requests and disconnect operations
remain in the official client. The adapter and protocol objects stay internal.

Construction raises `TypeError` when the expected dictionary is unavailable;
it must not continue with silently broken delivery. That check alone cannot
detect semantic changes to upstream dispatch, so dependency updates also need
the regression checks below.

Channel mapping is not an authorization boundary. Hosting must still enforce
project isolation and RLS before delivering a message. Do not broaden matching
to compensate for an authorization or server-routing bug.

## Why a public override does not remove it

As inspected on September 19, 2026, upstream
[`client.py` at 972489b6](https://github.com/centrifugal/centrifuge-python/blob/972489b6affeb83248ff7c883bd9b88df76ac669/centrifuge/client.py)
uses private subscription lookups in incoming-message paths. Overriding public
`get_subscription()` does not intercept all those paths; `subscriptions()`
returns a copy. No upstream fix or release commitment is assumed.

Remove the adapter when either a released public channel-routing extension
covers those paths, or a coordinated Hosting wire-channel change makes direct
lookup correct. A server change needs all three SDKs and an isolation review.
Moving the same private access into a subclass or copying the protocol client
is not removal.

## Review and verification

SDK maintainers must review this exception by **October 19, 2026**, and before
any dependency-range widening or Python SDK 1.0 release, whichever comes first.
Record the removal plan or an explicit reviewed renewal in VOL-1054. The deadline
does not extend automatically.

Every dependency update and server channel-shape change must:

1. Run deterministic generation, lint, typing, native tests, build and installed
   package checks from CI. The native realtime tests use both controlled fakes
   and the installed official client; preserve the latter's dispatch and
   lifecycle coverage.
2. Exercise broadcast, presence, Postgres/RLS routing, recovery, pause/resume,
   subscription removal and disconnect. Reject delivery from obsolete session
   or subscription epochs.
3. Before release, run shared realtime requirements `SDK-REALTIME-001` through
   `SDK-REALTIME-004` in an explicitly approved disposable environment and record
   the exact Hosting, SDK and dependency versions. Local dry runs are not live
   acceptance. A failing adapter check blocks the dependency update.
4. Obtain clean code and security reviews. Removing the adapter must also remove
   direct `_subs` access and update this document and the README.

## Existing evidence

[Acceptance run 35453946034](https://github.com/Kong/volcano-hosting/actions/runs/35453946034)
passed all 43 shared scenarios for Python revision
`12e978338fe1309c8e337362d3af26d4c70ff0a2`, using its locked `centrifuge-python`
0.6.0, against Hosting `3a243aa86792f8d6e81c36c900e485d2529ccc6f`.
That run predates the final Hosting merge; it does not validate a newer
dependency, a deployed main revision, or a future channel-routing change.

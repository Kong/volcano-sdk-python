from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from threading import Event, Thread

import pytest
from typing_extensions import override

from volcano_sdk import Session, VolcanoError
from volcano_sdk._session_operations import SessionOperations

SESSION = Session("access", "refresh", "user")


def test_first_refresh_completes_without_waiting_for_itself() -> None:
    operations = SessionOperations(SESSION)
    outcome: list[Session] = []

    def run() -> None:
        outcome.append(operations.refresh(lambda: SESSION))

    worker = Thread(target=run, daemon=True)
    worker.start()
    worker.join(2)

    assert not worker.is_alive()
    assert outcome == [SESSION]


def test_first_sign_out_completes_without_waiting_for_itself() -> None:
    operations = SessionOperations(SESSION)
    completed: list[bool] = []
    revocations: list[tuple[Future[Session] | None, bool]] = []

    def run() -> None:
        operations.sign_out(
            lambda preceding, pending: revocations.append((preceding, pending))
        )
        completed.append(True)

    worker = Thread(target=run, daemon=True)
    worker.start()
    worker.join(2)

    assert not worker.is_alive()
    assert completed == [True]
    assert revocations == [(None, False)]


def test_reentrant_refresh_fails_instead_of_waiting_for_its_owner() -> None:
    operations = SessionOperations(SESSION)
    failures: list[str] = []

    def run() -> None:
        try:
            _ = operations.refresh(lambda: operations.refresh(lambda: SESSION))
        except RuntimeError as error:
            failures.append(str(error))

    worker = Thread(target=run, daemon=True)
    worker.start()
    worker.join(2)

    assert not worker.is_alive()
    assert failures == ["Reentrant refresh"]


def test_reentrant_sign_out_fails_instead_of_waiting_for_its_owner() -> None:
    operations = SessionOperations(SESSION)
    failures: list[str] = []

    def run() -> None:
        try:
            operations.sign_out(
                lambda _preceding, _pending: operations.sign_out(
                    lambda _other_preceding, _other_pending: None
                )
            )
        except RuntimeError as error:
            failures.append(str(error))

    worker = Thread(target=run, daemon=True)
    worker.start()
    worker.join(2)

    assert not worker.is_alive()
    assert failures == ["Reentrant sign-out"]


class JoinedRefresh(Future[Session]):
    def __init__(self, joined: Event) -> None:
        super().__init__()
        self.joined: Event = joined

    @override
    def result(self, timeout: float | None = None) -> Session:
        self.joined.set()
        return super().result(timeout)


def operations_with_pending_refresh(pending: Future[Session]) -> SessionOperations:
    operations = SessionOperations(SESSION)
    operations.refreshing = pending
    return operations


@pytest.mark.parametrize("fails", [False, True])
def test_refresh_joins_pending_work_without_starting_another_operation(
    *, fails: bool
) -> None:
    joined = Event()
    pending = JoinedRefresh(joined)
    operations = operations_with_pending_refresh(pending)
    failure = RuntimeError("refresh failed")

    def unexpected_refresh() -> Session:
        pytest.fail("a joined refresh must not issue another request")

    with ThreadPoolExecutor(max_workers=1) as pool:
        waiter = pool.submit(operations.refresh, unexpected_refresh)
        try:
            assert joined.wait(2)
        finally:
            if fails:
                pending.set_exception(failure)
            else:
                pending.set_result(SESSION)
        if fails:
            with pytest.raises(RuntimeError, match="refresh failed") as error:
                _ = waiter.result(2)
            assert error.value is failure
        else:
            assert waiter.result(2) is SESSION


def test_refresh_completion_after_revocation_does_not_restore_credentials() -> None:
    pending: Future[Session] = Future()
    operations = operations_with_pending_refresh(pending)
    operations.clear_local_credentials()
    revocations: list[tuple[Future[Session] | None, bool]] = []

    def revoke(preceding: Future[Session] | None, *, pending: bool) -> None:
        revocations.append((preceding, pending))

    operations.sign_out(lambda preceding, pending: revoke(preceding, pending=pending))
    pending.set_result(SESSION)

    assert revocations == [(pending, True)]
    assert operations.refreshing is None
    assert not operations.has_verified_pair(SESSION)


@pytest.mark.parametrize("exception_type", [RuntimeError, KeyboardInterrupt])
def test_sign_out_replays_non_sdk_failures_without_retaining_request_frames(
    exception_type: type[BaseException],
) -> None:
    operations = SessionOperations(SESSION)
    original = exception_type("revocation interrupted")
    cause = VolcanoError("service unavailable", status=503, code="busy", retry_after=2)
    cause.__cause__ = RuntimeError("request frames")
    original.__cause__ = cause
    invocations: list[bool] = []

    def revoke(preceding: Future[Session] | None, *, pending: bool) -> None:
        assert preceding is None
        invocations.append(pending)
        raise original

    with pytest.raises(exception_type, match="revocation interrupted") as first:
        operations.sign_out(
            lambda preceding, pending: revoke(preceding, pending=pending)
        )
    with pytest.raises(exception_type, match="revocation interrupted") as second:
        operations.sign_out(
            lambda preceding, pending: revoke(preceding, pending=pending)
        )

    assert first.value is original
    assert second.value is not original
    assert second.value.args == original.args
    assert invocations == [False]
    assert operations.signing_out is not None
    template = operations.signing_out.result()
    assert template is not None
    assert template is not original
    assert template is not second.value
    assert template.__traceback__ is None
    assert template.__context__ is None
    copied_cause = template.__cause__
    assert isinstance(copied_cause, VolcanoError)
    assert copied_cause is not cause
    assert copied_cause.args == cause.args
    assert (copied_cause.status, copied_cause.code, copied_cause.retry_after) == (
        503,
        "busy",
        2,
    )
    assert copied_cause.__cause__ is None
    assert copied_cause.__traceback__ is None
    assert copied_cause.__context__ is None
    assert not operations.has_verified_pair(SESSION)


def test_sign_out_copy_stops_at_one_sdk_cause() -> None:
    operations = SessionOperations(SESSION)
    original = RuntimeError("revocation failed")
    upstream = VolcanoError("upstream failed", status=503)
    upstream.__cause__ = VolcanoError("nested request", status=500)
    original.__cause__ = upstream

    def revoke() -> None:
        raise original

    with pytest.raises(RuntimeError):
        operations.sign_out(lambda _preceding, _pending: revoke())
    with pytest.raises(RuntimeError) as replayed:
        operations.sign_out(lambda _preceding, _pending: revoke())

    copied_cause = replayed.value.__cause__
    assert isinstance(copied_cause, VolcanoError)
    assert copied_cause is not upstream
    assert copied_cause.status == 503
    assert copied_cause.__cause__ is None

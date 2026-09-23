from __future__ import annotations

import time
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, TypeVar
from uuid import uuid4

from volcano_sdk import VolcanoClient

if TYPE_CHECKING:
    from collections.abc import Callable

    from contract_support import ContractWorld

    from volcano_sdk.models import JSONValue, LogActivityResponse

_ResultT = TypeVar("_ResultT")

LOG_EVENT_COUNT = 3
ACTIVITY_BUCKET_COUNT = 2
HTTP_OK = 200


def poll(
    operation: Callable[[], _ResultT],
    ready: Callable[[_ResultT], bool],
    seconds: int,
) -> _ResultT:
    deadline = time.monotonic() + seconds
    while True:
        result = operation()
        if ready(result):
            return result
        assert time.monotonic() < deadline, (
            "matching logs did not arrive before deadline"
        )
        time.sleep(min(1, max(0, deadline - time.monotonic())))


def event_id(event: Mapping[str, JSONValue]) -> str:
    identity = event["id"]
    assert isinstance(identity, str)
    return identity


def mapping_field(
    value: Mapping[str, JSONValue], field: str
) -> Mapping[str, JSONValue]:
    nested = value[field]
    assert isinstance(nested, Mapping)
    return nested


def event_ordinal(event: Mapping[str, JSONValue]) -> int:
    ordinal = mapping_field(event, "body")["ordinal"]
    assert isinstance(ordinal, int)
    return ordinal


def bucket_count(bucket: Mapping[str, JSONValue], category: str, key: str) -> int:
    counts = mapping_field(bucket, "counts")
    value = mapping_field(counts, category).get(key, 0)
    assert isinstance(value, int)
    return value


def bucket_total(bucket: Mapping[str, JSONValue]) -> int:
    total = bucket["total"]
    assert isinstance(total, int)
    return total


class LogContract:
    def __init__(self, world: ContractWorld) -> None:
        self.world = world
        self.client = VolcanoClient(
            api_url=world.fixture["api_url"],
            anon_key=world.fixture["anon_key"],
            access_token=world.fixture["logs_access_token"],
            timeout=10,
        )
        self.marker = f"sdklogs{uuid4().hex}"
        self.request: dict[str, JSONValue] = {
            "resource": {"type": "function", "ids": [world.fixture["function_id"]]},
            "q": self.marker,
            "start_time": (datetime.now(UTC) - timedelta(minutes=5)).isoformat(),
        }

    def emit(self, count: int) -> None:
        for ordinal in range(count):
            response = self.world.service_client.functions.invoke(
                self.world.fixture["function_name"],
                {
                    "value": "contract",
                    "log_marker": self.marker,
                    "log_ordinal": ordinal,
                },
            )
            assert response.status == HTTP_OK
            assert response.data == {"echoed": "contract"}
        self.request["end_time"] = (
            datetime.now(UTC) + timedelta(minutes=5)
        ).isoformat()

    def search(self) -> list[Mapping[str, JSONValue]]:
        project = self.world.fixture["project_id"]
        page = poll(
            lambda: self.client.logs.search(project, {**self.request, "limit": 100}),
            lambda result: len(result.data) >= LOG_EVENT_COUNT,
            240,
        )
        assert len(page.data) == LOG_EVENT_COUNT
        expected_ids = {event_id(event) for event in page.data}
        events: list[Mapping[str, JSONValue]] = []
        request = {**self.request, "limit": 1}
        for _ in range(LOG_EVENT_COUNT):
            page = self.client.logs.search(project, request)
            assert page.limit == 1
            assert len(page.data) == 1
            events.extend(page.data)
            if not page.has_more:
                break
            assert page.next_cursor
            request = {**request, "cursor": page.next_cursor}
        assert not page.has_more
        assert {event_id(event) for event in events} == expected_ids
        return events

    def activity(self) -> LogActivityResponse:
        return poll(
            lambda: self.client.logs.activity(
                self.world.fixture["project_id"], {**self.request, "bucket_count": 2}
            ),
            lambda response: response.total >= 1,
            120,
        )

    def verify_events(self, events: list[Mapping[str, JSONValue]]) -> None:
        assert len(events) == LOG_EVENT_COUNT
        assert len({event_id(event) for event in events}) == LOG_EVENT_COUNT
        assert sorted(event_ordinal(event) for event in events) == [0, 1, 2]
        timestamps: list[datetime] = []
        for event in events:
            assert event["id"]
            body = mapping_field(event, "body")
            assert body == {
                "marker": self.marker,
                "ordinal": event_ordinal(event),
            }
            resource = mapping_field(event, "resource")
            assert resource["type"] == "function"
            assert resource["id"] == self.world.fixture["function_id"]
            assert event["level"] == "info"
            timestamp = event["timestamp"]
            assert isinstance(timestamp, str)
            timestamps.append(datetime.fromisoformat(timestamp))
        assert timestamps == sorted(timestamps, reverse=True)

    def verify_activity(self, response: LogActivityResponse) -> None:
        assert response.total == 1
        assert len(response.data) == ACTIVITY_BUCKET_COUNT
        assert sum(bucket_total(bucket) for bucket in response.data) == 1
        assert (
            sum(
                bucket_count(bucket, "resource_ids", self.world.fixture["function_id"])
                for bucket in response.data
            )
            == 1
        )
        assert (
            sum(bucket_count(bucket, "levels", "info") for bucket in response.data) == 1
        )

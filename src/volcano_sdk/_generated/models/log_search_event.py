from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.live_log_level import check_live_log_level
from ..models.live_log_level import LiveLogLevel
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.log_deployment import LogDeployment
  from ..models.log_event_body_type_1 import LogEventBodyType1
  from ..models.log_resource import LogResource





T = TypeVar("T", bound="LogSearchEvent")



@_attrs_define
class LogSearchEvent:
    """ 
        Attributes:
            timestamp (datetime.datetime): Event timestamp.
            body (bool | float | list[Any] | LogEventBodyType1 | None | str): Application log value. JSON arguments retain
                their JSON type. Strings containing a serialized JSON object or array are normalized to that object or array;
                all other strings remain strings.
            id (str): Opaque stable log event ID for pagination, deduplication, and display.
            resource (LogResource): Resource that owns a historical log event.
            level (LiveLogLevel | Unset): Canonical lowercase function runtime log level.
            region (str | Unset): Region where this log event originated.
            deployment (LogDeployment | Unset): Deployment context associated with a historical deployment log event.
            invocation_id (str | Unset): Function invocation ID associated with this log event, when available.
     """

    timestamp: datetime.datetime
    body: bool | float | list[Any] | LogEventBodyType1 | None | str
    id: str
    resource: LogResource
    level: LiveLogLevel | Unset = UNSET
    region: str | Unset = UNSET
    deployment: LogDeployment | Unset = UNSET
    invocation_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.log_deployment import LogDeployment
        from ..models.log_event_body_type_1 import LogEventBodyType1
        from ..models.log_resource import LogResource
        timestamp = self.timestamp.isoformat()

        body: bool | dict[str, Any] | float | list[Any] | None | str
        if isinstance(self.body, LogEventBodyType1):
            body = self.body.to_dict()
        elif isinstance(self.body, list):
            body = self.body


        else:
            body = self.body

        id = self.id

        resource = self.resource.to_dict()

        level: str | Unset = UNSET
        if not isinstance(self.level, Unset):
            level = self.level


        region = self.region

        deployment: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deployment, Unset):
            deployment = self.deployment.to_dict()

        invocation_id = self.invocation_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "timestamp": timestamp,
            "body": body,
            "id": id,
            "resource": resource,
        })
        if level is not UNSET:
            field_dict["level"] = level
        if region is not UNSET:
            field_dict["region"] = region
        if deployment is not UNSET:
            field_dict["deployment"] = deployment
        if invocation_id is not UNSET:
            field_dict["invocation_id"] = invocation_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_deployment import LogDeployment
        from ..models.log_event_body_type_1 import LogEventBodyType1
        from ..models.log_resource import LogResource
        d = dict(src_dict)
        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))




        def _parse_body(data: object) -> bool | float | list[Any] | LogEventBodyType1 | None | str:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                body_type_1 = LogEventBodyType1.from_dict(data)



                return body_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                body_type_2 = cast(list[Any], data)

                return body_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(bool | float | list[Any] | LogEventBodyType1 | None | str, data)

        body = _parse_body(d.pop("body"))


        id = d.pop("id")

        resource = LogResource.from_dict(d.pop("resource"))




        _level = d.pop("level", UNSET)
        level: LiveLogLevel | Unset
        if isinstance(_level,  Unset):
            level = UNSET
        else:
            level = check_live_log_level(_level)




        region = d.pop("region", UNSET)

        _deployment = d.pop("deployment", UNSET)
        deployment: LogDeployment | Unset
        if isinstance(_deployment,  Unset):
            deployment = UNSET
        else:
            deployment = LogDeployment.from_dict(_deployment)




        invocation_id = d.pop("invocation_id", UNSET)

        log_search_event = cls(
            timestamp=timestamp,
            body=body,
            id=id,
            resource=resource,
            level=level,
            region=region,
            deployment=deployment,
            invocation_id=invocation_id,
        )


        log_search_event.additional_properties = d
        return log_search_event

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.log_database_request_resource import LogDatabaseRequestResource
  from ..models.log_frontend_request_resource import LogFrontendRequestResource
  from ..models.log_function_request_resource import LogFunctionRequestResource





T = TypeVar("T", bound="LogStreamRequest")



@_attrs_define
class LogStreamRequest:
    """ Stream request for live project logs. Pagination cursors and fixed end times are not supported.

        Attributes:
            resource (LogDatabaseRequestResource | LogFrontendRequestResource | LogFunctionRequestResource): Resource
                selectors for project log reads.
            q (str | Unset): Optional log query using the same syntax as search and activity requests.
            start_time (datetime.datetime | Unset): Start time.
            limit (int | Unset): Maximum number of records to deliver on connect or reconnect before following new events.
                Default: 100.
     """

    resource: LogDatabaseRequestResource | LogFrontendRequestResource | LogFunctionRequestResource
    q: str | Unset = UNSET
    start_time: datetime.datetime | Unset = UNSET
    limit: int | Unset = 100





    def to_dict(self) -> dict[str, Any]:
        from ..models.log_database_request_resource import LogDatabaseRequestResource
        from ..models.log_frontend_request_resource import LogFrontendRequestResource
        from ..models.log_function_request_resource import LogFunctionRequestResource
        resource: dict[str, Any]
        if isinstance(self.resource, LogFunctionRequestResource):
            resource = self.resource.to_dict()
        elif isinstance(self.resource, LogFrontendRequestResource):
            resource = self.resource.to_dict()
        else:
            resource = self.resource.to_dict()


        q = self.q

        start_time: str | Unset = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        limit = self.limit


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "resource": resource,
        })
        if q is not UNSET:
            field_dict["q"] = q
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_database_request_resource import LogDatabaseRequestResource
        from ..models.log_frontend_request_resource import LogFrontendRequestResource
        from ..models.log_function_request_resource import LogFunctionRequestResource
        d = dict(src_dict)
        def _parse_resource(data: object) -> LogDatabaseRequestResource | LogFrontendRequestResource | LogFunctionRequestResource:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_log_request_resource_type_0 = LogFunctionRequestResource.from_dict(data)



                return componentsschemas_log_request_resource_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_log_request_resource_type_1 = LogFrontendRequestResource.from_dict(data)



                return componentsschemas_log_request_resource_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_log_request_resource_type_2 = LogDatabaseRequestResource.from_dict(data)



            return componentsschemas_log_request_resource_type_2

        resource = _parse_resource(d.pop("resource"))


        q = d.pop("q", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: datetime.datetime | Unset
        if isinstance(_start_time,  Unset):
            start_time = UNSET
        else:
            start_time = datetime.datetime.fromisoformat(_start_time)




        limit = d.pop("limit", UNSET)

        log_stream_request = cls(
            resource=resource,
            q=q,
            start_time=start_time,
            limit=limit,
        )

        return log_stream_request


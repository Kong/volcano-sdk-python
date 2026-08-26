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





T = TypeVar("T", bound="LogActivityRequest")



@_attrs_define
class LogActivityRequest:
    """ Activity request for bucketed log counts.

        Attributes:
            resource (LogDatabaseRequestResource | LogFrontendRequestResource | LogFunctionRequestResource): Resource
                selectors for project log reads.
            q (str | Unset): Optional activity query. Supports quoted text, implicit AND, AND/OR/NOT, parentheses, and
                fields such as `level`, `region`, `invocation.id`, `resource.id`, `resource.name`, `function`, `frontend`,
                `database`, and `body`.
            start_time (datetime.datetime | Unset): Start time.
            end_time (datetime.datetime | Unset): End time.
            bucket_count (int | Unset): Number of activity buckets to return.
     """

    resource: LogDatabaseRequestResource | LogFrontendRequestResource | LogFunctionRequestResource
    q: str | Unset = UNSET
    start_time: datetime.datetime | Unset = UNSET
    end_time: datetime.datetime | Unset = UNSET
    bucket_count: int | Unset = UNSET





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

        end_time: str | Unset = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        bucket_count = self.bucket_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "resource": resource,
        })
        if q is not UNSET:
            field_dict["q"] = q
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if bucket_count is not UNSET:
            field_dict["bucket_count"] = bucket_count

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




        _end_time = d.pop("end_time", UNSET)
        end_time: datetime.datetime | Unset
        if isinstance(_end_time,  Unset):
            end_time = UNSET
        else:
            end_time = datetime.datetime.fromisoformat(_end_time)




        bucket_count = d.pop("bucket_count", UNSET)

        log_activity_request = cls(
            resource=resource,
            q=q,
            start_time=start_time,
            end_time=end_time,
            bucket_count=bucket_count,
        )

        return log_activity_request


from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.lavaflow_anomaly import LavaflowAnomaly
  from ..models.lavaflow_resource_reference import LavaflowResourceReference





T = TypeVar("T", bound="LavaflowResource")



@_attrs_define
class LavaflowResource:
    """ 
        Attributes:
            project_id (UUID): The project the resource belongs to.
            resource (LavaflowResourceReference): A function, durable function or frontend in the project, or the project of
                a user-reported problem.
            last_analyzed_at (datetime.datetime | None): When a LavaFlow run last started on the resource, null if never.
            issues_opened (int): Issues LavaFlow took on in the window.
            pull_requests_opened (int): Pull requests with a fix LavaFlow opened in the window.
            anomaly (LavaflowAnomaly):
     """

    project_id: UUID
    resource: LavaflowResourceReference
    last_analyzed_at: datetime.datetime | None
    issues_opened: int
    pull_requests_opened: int
    anomaly: LavaflowAnomaly
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_anomaly import LavaflowAnomaly # noqa: PLC0415
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        project_id = str(self.project_id)

        resource = self.resource.to_dict()

        last_analyzed_at: None | str
        if isinstance(self.last_analyzed_at, datetime.datetime):
            last_analyzed_at = self.last_analyzed_at.isoformat()
        else:
            last_analyzed_at = self.last_analyzed_at

        issues_opened = self.issues_opened

        pull_requests_opened = self.pull_requests_opened

        anomaly = self.anomaly.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "project_id": project_id,
            "resource": resource,
            "last_analyzed_at": last_analyzed_at,
            "issues_opened": issues_opened,
            "pull_requests_opened": pull_requests_opened,
            "anomaly": anomaly,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_anomaly import LavaflowAnomaly # noqa: PLC0415
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))




        resource = LavaflowResourceReference.from_dict(d.pop("resource"))




        def _parse_last_analyzed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_analyzed_at_type_0 = datetime.datetime.fromisoformat(data)



                return last_analyzed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_analyzed_at = _parse_last_analyzed_at(d.pop("last_analyzed_at"))


        issues_opened = d.pop("issues_opened")

        pull_requests_opened = d.pop("pull_requests_opened")

        anomaly = LavaflowAnomaly.from_dict(d.pop("anomaly"))




        lavaflow_resource = cls(
            project_id=project_id,
            resource=resource,
            last_analyzed_at=last_analyzed_at,
            issues_opened=issues_opened,
            pull_requests_opened=pull_requests_opened,
            anomaly=anomaly,
        )


        lavaflow_resource.additional_properties = d
        return lavaflow_resource

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

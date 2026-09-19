from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.project_access_token_usage_daily_entry import ProjectAccessTokenUsageDailyEntry





T = TypeVar("T", bound="ProjectAccessTokenUsage")



@_attrs_define
class ProjectAccessTokenUsage:
    """ Zero-filled daily request counts for a single token, oldest first. Every
    day in the window is present, so a gap reads as zero rather than missing.

    Counts every request the token authenticated, including ones then
    refused — a read-only token attempting a write, or a token presented on
    another project's route. That is deliberate: after a leak, the probing
    is the part you want to see, and a counter that hid it would make a
    token look idle while it was being tried.

        Attributes:
            token_id (UUID):
            name (str):
            token_prefix (str): The token's display prefix, which identifies the credential when its
                name does not. Revoking frees a name, so a project that rotated
                `ci-deploy` has two entries here both called `ci-deploy`. Not usable
                as a credential.
            days (int): Number of daily entries returned, always equal to the requested window.
            daily (list[ProjectAccessTokenUsageDailyEntry]):
            total_requests (int):
     """

    token_id: UUID
    name: str
    token_prefix: str
    days: int
    daily: list[ProjectAccessTokenUsageDailyEntry]
    total_requests: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_access_token_usage_daily_entry import ProjectAccessTokenUsageDailyEntry
        token_id = str(self.token_id)

        name = self.name

        token_prefix = self.token_prefix

        days = self.days

        daily = []
        for daily_item_data in self.daily:
            daily_item = daily_item_data.to_dict()
            daily.append(daily_item)



        total_requests = self.total_requests


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "token_id": token_id,
            "name": name,
            "token_prefix": token_prefix,
            "days": days,
            "daily": daily,
            "total_requests": total_requests,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_access_token_usage_daily_entry import ProjectAccessTokenUsageDailyEntry
        d = dict(src_dict)
        token_id = UUID(d.pop("token_id"))




        name = d.pop("name")

        token_prefix = d.pop("token_prefix")

        days = d.pop("days")

        daily = []
        _daily = d.pop("daily")
        for daily_item_data in (_daily):
            daily_item = ProjectAccessTokenUsageDailyEntry.from_dict(daily_item_data)



            daily.append(daily_item)


        total_requests = d.pop("total_requests")

        project_access_token_usage = cls(
            token_id=token_id,
            name=name,
            token_prefix=token_prefix,
            days=days,
            daily=daily,
            total_requests=total_requests,
        )


        project_access_token_usage.additional_properties = d
        return project_access_token_usage

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_app_request_resource_type import check_log_app_request_resource_type
from ..models.log_app_request_resource_type import LogAppRequestResourceType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LogAppRequestResource")



@_attrs_define
class LogAppRequestResource:
    """ Selector for the entries a first-party app writes into this project's
    logs, such as the Builder's run lifecycle. Each app is one resource.
    Its ID is UUIDv5(`7374f5e9-35ff-4e46-ac13-a4717bae00e1`, slug), with
    the app's slug as UTF-8 bytes, and its name is the slug. The Builder
    (`builder`) is `b52fc8fa-8656-5141-adef-99d698ce6f3c`. Deployment logs
    are not supported for apps.

        Attributes:
            type_ (LogAppRequestResourceType): Resource type to read logs for.
            ids (list[UUID] | Unset): Optional app resource IDs, each UUIDv5 of an app's slug. Omit or send an empty array
                to include every app.
     """

    type_: LogAppRequestResourceType
    ids: list[UUID] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        ids: list[str] | Unset = UNSET
        if not isinstance(self.ids, Unset):
            ids = []
            for ids_item_data in self.ids:
                ids_item = str(ids_item_data)
                ids.append(ids_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })
        if ids is not UNSET:
            field_dict["ids"] = ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_log_app_request_resource_type(d.pop("type"))




        _ids = d.pop("ids", UNSET)
        ids: list[UUID] | Unset = UNSET
        if _ids is not UNSET:
            ids = []
            for ids_item_data in _ids:
                ids_item = UUID(ids_item_data)



                ids.append(ids_item)


        log_app_request_resource = cls(
            type_=type_,
            ids=ids,
        )

        return log_app_request_resource


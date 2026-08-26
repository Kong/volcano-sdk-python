from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_database_request_resource_type import check_log_database_request_resource_type
from ..models.log_database_request_resource_type import LogDatabaseRequestResourceType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LogDatabaseRequestResource")



@_attrs_define
class LogDatabaseRequestResource:
    """ Database runtime log resource selector. Deployment logs are not supported for databases.

        Attributes:
            type_ (LogDatabaseRequestResourceType): Resource type to read logs for.
            ids (list[UUID] | Unset): Optional database identifiers. Omit or send an empty array to include every database
                in the project.
     """

    type_: LogDatabaseRequestResourceType
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
        type_ = check_log_database_request_resource_type(d.pop("type"))




        _ids = d.pop("ids", UNSET)
        ids: list[UUID] | Unset = UNSET
        if _ids is not UNSET:
            ids = []
            for ids_item_data in _ids:
                ids_item = UUID(ids_item_data)



                ids.append(ids_item)


        log_database_request_resource = cls(
            type_=type_,
            ids=ids,
        )

        return log_database_request_resource


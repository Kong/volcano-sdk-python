from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LogDeploymentRequestSelector")



@_attrs_define
class LogDeploymentRequestSelector:
    """ Deployment log selector for deployable resources.

        Attributes:
            ids (list[UUID] | Unset): Optional deployment identifiers. Omit or send an empty array to include every
                deployment for the selected resources.
     """

    ids: list[UUID] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        ids: list[str] | Unset = UNSET
        if not isinstance(self.ids, Unset):
            ids = []
            for ids_item_data in self.ids:
                ids_item = str(ids_item_data)
                ids.append(ids_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if ids is not UNSET:
            field_dict["ids"] = ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _ids = d.pop("ids", UNSET)
        ids: list[UUID] | Unset = UNSET
        if _ids is not UNSET:
            ids = []
            for ids_item_data in _ids:
                ids_item = UUID(ids_item_data)



                ids.append(ids_item)


        log_deployment_request_selector = cls(
            ids=ids,
        )

        return log_deployment_request_selector


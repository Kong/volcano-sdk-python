from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ShareReleaseCreateRequest")



@_attrs_define
class ShareReleaseCreateRequest:
    """ 
        Attributes:
            share_id (str): The share to publish to. Its own project authorizes the publish.
            draft_id (str): The `draft_id` of the draft the owner reviewed. If a fresh build of the
                project is not that draft, nothing is published and the answer is `409`
                `draft_changed` with the new draft.
            variables (list[str]): Every name in the draft's `variables`, which a project created from the
                release gets. Values are never carried: each is created empty unless the
                visitor gives one.
            service_key_functions (list[str]): The functions that receive the new project's `VOLCANO_SERVICE_KEY`, which
                bypasses row-level security. Must be exactly the draft's
                `service_key_functions`.
     """

    share_id: str
    draft_id: str
    variables: list[str]
    service_key_functions: list[str]





    def to_dict(self) -> dict[str, Any]:
        share_id = self.share_id

        draft_id = self.draft_id

        variables = self.variables



        service_key_functions = self.service_key_functions




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "share_id": share_id,
            "draft_id": draft_id,
            "variables": variables,
            "service_key_functions": service_key_functions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        share_id = d.pop("share_id")

        draft_id = d.pop("draft_id")

        variables = cast(list[str], d.pop("variables"))


        service_key_functions = cast(list[str], d.pop("service_key_functions"))


        share_release_create_request = cls(
            share_id=share_id,
            draft_id=draft_id,
            variables=variables,
            service_key_functions=service_key_functions,
        )

        return share_release_create_request


from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.fork_create_request_variables import ForkCreateRequestVariables





T = TypeVar("T", bound="ForkCreateRequest")



@_attrs_define
class ForkCreateRequest:
    """ 
        Attributes:
            share_id (str): The share to fork, the id at the end of its deploy URL.
            release_id (UUID): The `release.id` the share's preview returned, so only the release the visitor saw is
                installed.
            name (str): The new project's name, which may contain only letters, numbers, underscores and hyphens. A name you
                already use gets a short random suffix. An invalid name answers `400` before anything is counted against the
                share or your hourly fork limit.
            variables (ForkCreateRequestVariables | Unset): Values for the variables the preview lists, by name. Any may be
                left out
                and is then created empty; only listed names are accepted (`422`
                otherwise). Each value is at most 4096 bytes of UTF-8, since a function's
                environment is limited in bytes; a longer one, or one containing a NUL
                character, answers `400`. Values are never logged, and `Idempotency-Key` compares only the names given a value.
     """

    share_id: str
    release_id: UUID
    name: str
    variables: ForkCreateRequestVariables | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.fork_create_request_variables import ForkCreateRequestVariables # noqa: PLC0415
        share_id = self.share_id

        release_id = str(self.release_id)

        name = self.name

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "share_id": share_id,
            "release_id": release_id,
            "name": name,
        })
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fork_create_request_variables import ForkCreateRequestVariables # noqa: PLC0415
        d = dict(src_dict)
        share_id = d.pop("share_id")

        release_id = UUID(d.pop("release_id"))




        name = d.pop("name")

        _variables = d.pop("variables", UNSET)
        variables: ForkCreateRequestVariables | Unset
        if isinstance(_variables,  Unset):
            variables = UNSET
        else:
            variables = ForkCreateRequestVariables.from_dict(_variables)




        fork_create_request = cls(
            share_id=share_id,
            release_id=release_id,
            name=name,
            variables=variables,
        )

        return fork_create_request


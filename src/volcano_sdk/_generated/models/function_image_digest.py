from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="FunctionImageDigest")



@_attrs_define
class FunctionImageDigest:
    """ The content digest of a function image in one region. It names no registry or account.

        Attributes:
            digest (str):
            region (str | Unset): The region the image was published to. Absent when the build published one image for every
                region.
     """

    digest: str
    region: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        digest = self.digest

        region = self.region


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "digest": digest,
        })
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        digest = d.pop("digest")

        region = d.pop("region", UNSET)

        function_image_digest = cls(
            digest=digest,
            region=region,
        )

        return function_image_digest


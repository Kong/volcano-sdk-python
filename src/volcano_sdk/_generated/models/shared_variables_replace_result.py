from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.skipped_served_function import SkippedServedFunction





T = TypeVar("T", bound="SharedVariablesReplaceResult")



@_attrs_define
class SharedVariablesReplaceResult:
    """ 
        Attributes:
            skipped_functions (list[SkippedServedFunction]): Functions the replacement changes whose variables were not
                synchronized.
     """

    skipped_functions: list[SkippedServedFunction]





    def to_dict(self) -> dict[str, Any]:
        from ..models.skipped_served_function import SkippedServedFunction # noqa: PLC0415
        skipped_functions = []
        for skipped_functions_item_data in self.skipped_functions:
            skipped_functions_item = skipped_functions_item_data.to_dict()
            skipped_functions.append(skipped_functions_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "skipped_functions": skipped_functions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.skipped_served_function import SkippedServedFunction # noqa: PLC0415
        d = dict(src_dict)
        skipped_functions = []
        _skipped_functions = d.pop("skipped_functions")
        for skipped_functions_item_data in (_skipped_functions):
            skipped_functions_item = SkippedServedFunction.from_dict(skipped_functions_item_data)



            skipped_functions.append(skipped_functions_item)


        shared_variables_replace_result = cls(
            skipped_functions=skipped_functions,
        )

        return shared_variables_replace_result


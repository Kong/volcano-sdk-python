from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_validation_error import ProjectConfigValidationError





T = TypeVar("T", bound="ProjectConfigValidationErrorResponse")



@_attrs_define
class ProjectConfigValidationErrorResponse:
    """ Returned when manifest validation fails. Nothing was applied.

        Attributes:
            error (str):
            errors (list[ProjectConfigValidationError]):
     """

    error: str
    errors: list[ProjectConfigValidationError]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_validation_error import ProjectConfigValidationError
        error = self.error

        errors = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
            "errors": errors,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_validation_error import ProjectConfigValidationError
        d = dict(src_dict)
        error = d.pop("error")

        errors = []
        _errors = d.pop("errors")
        for errors_item_data in (_errors):
            errors_item = ProjectConfigValidationError.from_dict(errors_item_data)



            errors.append(errors_item)


        project_config_validation_error_response = cls(
            error=error,
            errors=errors,
        )


        project_config_validation_error_response.additional_properties = d
        return project_config_validation_error_response

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

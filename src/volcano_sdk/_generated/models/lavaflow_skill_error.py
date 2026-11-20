from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_skill_error_rules_item import check_lavaflow_skill_error_rules_item
from ..models.lavaflow_skill_error_rules_item import LavaflowSkillErrorRulesItem
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="LavaflowSkillError")



@_attrs_define
class LavaflowSkillError:
    """ An error, with the rules a refused skill failed.

        Attributes:
            error (str):
            code (str | Unset): `skill_refused` means the skill check refused the text. `feature_unavailable` means the
                change needs the project's `lavaflow.skills` capability.
            rules (list[LavaflowSkillErrorRulesItem] | Unset): With `skill_refused`, the rules the text failed. The answer
                never repeats the text.
     """

    error: str
    code: str | Unset = UNSET
    rules: list[LavaflowSkillErrorRulesItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code = self.code

        rules: list[str] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item: str = rules_item_data
                rules.append(rules_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
        })
        if code is not UNSET:
            field_dict["code"] = code
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        code = d.pop("code", UNSET)

        _rules = d.pop("rules", UNSET)
        rules: list[LavaflowSkillErrorRulesItem] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = check_lavaflow_skill_error_rules_item(rules_item_data)



                rules.append(rules_item)


        lavaflow_skill_error = cls(
            error=error,
            code=code,
            rules=rules,
        )


        lavaflow_skill_error.additional_properties = d
        return lavaflow_skill_error

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

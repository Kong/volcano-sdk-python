from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="DatabaseMigrationConflictError")



@_attrs_define
class DatabaseMigrationConflictError:
    """ A migration request refused by the database's state. With code
    `migration_run_in_progress`, `run_id` names the run that is queued or
    running.

        Attributes:
            error (str):
            code (str | Unset): Stable machine-readable error code when a specific recovery path is available.
                `plan_required` (403) means the project owner's plan does not include the requested feature or option; upgrading
                the plan unlocks it. A 403 without a code leaves the reason unspecified: it can be an access refusal, a reached
                limit, or a plan check that could not read the owner's plan. Match on the code, not the message text.
            run_id (UUID | Unset):
     """

    error: str
    code: str | Unset = UNSET
    run_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code = self.code

        run_id: str | Unset = UNSET
        if not isinstance(self.run_id, Unset):
            run_id = str(self.run_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
        })
        if code is not UNSET:
            field_dict["code"] = code
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        code = d.pop("code", UNSET)

        _run_id = d.pop("run_id", UNSET)
        run_id: UUID | Unset
        if isinstance(_run_id,  Unset):
            run_id = UNSET
        else:
            run_id = UUID(_run_id)




        database_migration_conflict_error = cls(
            error=error,
            code=code,
            run_id=run_id,
        )


        database_migration_conflict_error.additional_properties = d
        return database_migration_conflict_error

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

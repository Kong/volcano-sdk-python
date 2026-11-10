from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="LavaflowRepositoryCheckCommand")



@_attrs_define
class LavaflowRepositoryCheckCommand:
    """ One command the repository's checks ran. `command` and `output` are the repository's own text, served as LavaFlow
    recorded it. `command` reads `LavaFlow left this command out because it may contain a credential`, and `output`
    reads `LavaFlow left this output out because it may contain a credential`, when that text may contain a credential,
    holds one of the project's secret values, or is over 4,000 characters, and when the run is held with
    `possible_credential`.

        Attributes:
            command (str): The command as LavaFlow ran it.
            status (str): `passed`: the command succeeded. `failed`: it exited with an error. `timed_out`: it ran past its
                time limit, and LavaFlow stopped it. Treat a status you don't know as `failed`.
            exit_code (int | None): The code the command exited with, null when it gave none, as a command that timed out
                may not.
            output (str | Unset): The end of what the command printed, present only when `status` is `failed` or `timed_out`
                and LavaFlow kept it; `""` when it printed nothing.
     """

    command: str
    status: str
    exit_code: int | None
    output: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        command = self.command

        status = self.status

        exit_code: int | None
        exit_code = self.exit_code

        output = self.output


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "command": command,
            "status": status,
            "exit_code": exit_code,
        })
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        command = d.pop("command")

        status = d.pop("status")

        def _parse_exit_code(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        exit_code = _parse_exit_code(d.pop("exit_code"))


        output = d.pop("output", UNSET)

        lavaflow_repository_check_command = cls(
            command=command,
            status=status,
            exit_code=exit_code,
            output=output,
        )


        lavaflow_repository_check_command.additional_properties = d
        return lavaflow_repository_check_command

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

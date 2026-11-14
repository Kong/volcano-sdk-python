from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_repository_check_command import LavaflowRepositoryCheckCommand





T = TypeVar("T", bound="LavaflowRepositoryChecks")



@_attrs_define
class LavaflowRepositoryChecks:
    """ Whether LavaFlow ran the repository's own checks, such as its tests, on a fix itself, before it opened a pull
    request or held the fix, and what they found. When LavaFlow ran them more than once, this is the last time the run's
    last attempt ran them; `not_run` when that attempt didn't, or while the run is queued or running. CI that runs on
    the pull request afterwards is the repository's own.

        Attributes:
            status (str): `passed`: every command the checks ran passed. `failed`: a command failed or timed out; `commands`
                shows which. `no_checks_found`: LavaFlow found no checks in the repository to run. `not_run`: LavaFlow did not
                run the repository's checks on the fix, for the reason `reason` names. Treat a status you don't know as
                `not_run`.
            message (str): Text to show for the status and reason. It names the pull request when one opened. For `not_run`
                on a fix whose pull request opened, a second sentence says what became of the repository's CI there, as the run
                stands when read: whether LavaFlow started it, tried to, may still, or won't.
            reason (str | Unset): Stable code for why the checks did not run, present only when `status` is `not_run`.
                `dependencies_changed`: the fix changes the repository's dependencies. `dependencies_not_installed`: LavaFlow
                couldn't install the repository's dependencies. `run_deadline`: the run reached its time limit.
                `sandbox_capacity`: no sandbox slot was free in time to run them. `sandbox_budget`: LavaFlow's sandbox allowance
                for checks was used up. `sandbox_not_isolated`: LavaFlow couldn't confirm the sandbox was isolated.
                `sandbox_plan_limit`: LavaFlow couldn't start a sandbox large enough to run them. `sandbox_unavailable`:
                LavaFlow couldn't run them itself. `source_too_large`: the repository is too large to copy into a sandbox.
                `source_unavailable`: LavaFlow couldn't fetch the fix's source to check it, as when the repository was
                disconnected or changed during the run. `tool_unavailable`: a tool the checks need isn't available. New reasons
                may appear; treat one you don't know like any other `not_run`.
            revised (bool | Unset): Present and `true` only when `status` is `failed` and LavaFlow then revised the fix once
                without running the checks again. `status` and `commands` describe that earlier version, not the fix as saved,
                which the checks never ran on.
            commands (list[LavaflowRepositoryCheckCommand] | Unset): The commands the checks ran, in order. Absent when
                LavaFlow recorded none, as for `no_checks_found` and `not_run`.
     """

    status: str
    message: str
    reason: str | Unset = UNSET
    revised: bool | Unset = UNSET
    commands: list[LavaflowRepositoryCheckCommand] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_repository_check_command import LavaflowRepositoryCheckCommand # noqa: PLC0415
        status = self.status

        message = self.message

        reason = self.reason

        revised = self.revised

        commands: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.commands, Unset):
            commands = []
            for commands_item_data in self.commands:
                commands_item = commands_item_data.to_dict()
                commands.append(commands_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "message": message,
        })
        if reason is not UNSET:
            field_dict["reason"] = reason
        if revised is not UNSET:
            field_dict["revised"] = revised
        if commands is not UNSET:
            field_dict["commands"] = commands

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_repository_check_command import LavaflowRepositoryCheckCommand # noqa: PLC0415
        d = dict(src_dict)
        status = d.pop("status")

        message = d.pop("message")

        reason = d.pop("reason", UNSET)

        revised = d.pop("revised", UNSET)

        _commands = d.pop("commands", UNSET)
        commands: list[LavaflowRepositoryCheckCommand] | Unset = UNSET
        if _commands is not UNSET:
            commands = []
            for commands_item_data in _commands:
                commands_item = LavaflowRepositoryCheckCommand.from_dict(commands_item_data)



                commands.append(commands_item)


        lavaflow_repository_checks = cls(
            status=status,
            message=message,
            reason=reason,
            revised=revised,
            commands=commands,
        )


        lavaflow_repository_checks.additional_properties = d
        return lavaflow_repository_checks

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

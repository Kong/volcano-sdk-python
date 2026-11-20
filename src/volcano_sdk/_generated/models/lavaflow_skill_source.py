from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_skill_source_act import check_lavaflow_skill_source_act
from ..models.lavaflow_skill_source_act import LavaflowSkillSourceAct
from ..models.lavaflow_skill_source_kind import check_lavaflow_skill_source_kind
from ..models.lavaflow_skill_source_kind import LavaflowSkillSourceKind
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="LavaflowSkillSource")



@_attrs_define
class LavaflowSkillSource:
    """ Where a version came from: a writer's act on a fix's pull request, or the owner's edit.

        Attributes:
            kind (LavaflowSkillSourceKind):
            run_id (None | UUID): The run whose pull request taught it, for `run`.
            pull_request (int | None): That run's pull request number.
            act (LavaflowSkillSourceAct): The writer's act it came from, for `run`.
            user_id (None | str): The person who edited it, for `person`.
     """

    kind: LavaflowSkillSourceKind
    run_id: None | UUID
    pull_request: int | None
    act: LavaflowSkillSourceAct
    user_id: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        run_id: None | str
        if isinstance(self.run_id, UUID):
            run_id = str(self.run_id)
        else:
            run_id = self.run_id

        pull_request: int | None
        pull_request = self.pull_request

        act: str = self.act

        user_id: None | str
        user_id = self.user_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "run_id": run_id,
            "pull_request": pull_request,
            "act": act,
            "user_id": user_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_lavaflow_skill_source_kind(d.pop("kind"))




        def _parse_run_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                run_id_type_0 = UUID(data)



                return run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        run_id = _parse_run_id(d.pop("run_id"))


        def _parse_pull_request(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        pull_request = _parse_pull_request(d.pop("pull_request"))


        act = check_lavaflow_skill_source_act(d.pop("act"))




        def _parse_user_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        user_id = _parse_user_id(d.pop("user_id"))


        lavaflow_skill_source = cls(
            kind=kind,
            run_id=run_id,
            pull_request=pull_request,
            act=act,
            user_id=user_id,
        )


        lavaflow_skill_source.additional_properties = d
        return lavaflow_skill_source

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

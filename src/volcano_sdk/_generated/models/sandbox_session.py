from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sandbox_session_desired_state import check_sandbox_session_desired_state
from ..models.sandbox_session_desired_state import SandboxSessionDesiredState
from ..models.sandbox_session_state import check_sandbox_session_state
from ..models.sandbox_session_state import SandboxSessionState
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="SandboxSession")



@_attrs_define
class SandboxSession:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            sandbox_id (UUID):
            state (SandboxSessionState):
            desired_state (SandboxSessionDesiredState):
            region (str):
            memory_mb (int):
            created_at (datetime.datetime):
            expires_at (datetime.datetime):
            started_at (datetime.datetime | Unset):
     """

    id: UUID
    project_id: UUID
    sandbox_id: UUID
    state: SandboxSessionState
    desired_state: SandboxSessionDesiredState
    region: str
    memory_mb: int
    created_at: datetime.datetime
    expires_at: datetime.datetime
    started_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        sandbox_id = str(self.sandbox_id)

        state: str = self.state

        desired_state: str = self.desired_state

        region = self.region

        memory_mb = self.memory_mb

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "project_id": project_id,
            "sandbox_id": sandbox_id,
            "state": state,
            "desired_state": desired_state,
            "region": region,
            "memory_mb": memory_mb,
            "created_at": created_at,
            "expires_at": expires_at,
        })
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        sandbox_id = UUID(d.pop("sandbox_id"))




        state = check_sandbox_session_state(d.pop("state"))




        desired_state = check_sandbox_session_desired_state(d.pop("desired_state"))




        region = d.pop("region")

        memory_mb = d.pop("memory_mb")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))




        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = datetime.datetime.fromisoformat(_started_at)




        sandbox_session = cls(
            id=id,
            project_id=project_id,
            sandbox_id=sandbox_id,
            state=state,
            desired_state=desired_state,
            region=region,
            memory_mb=memory_mb,
            created_at=created_at,
            expires_at=expires_at,
            started_at=started_at,
        )

        return sandbox_session


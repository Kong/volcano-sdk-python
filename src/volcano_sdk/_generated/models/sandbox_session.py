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
            sandbox_id (None | UUID): Explicit template used to create the session. Null when created directly from a
                preset.
            state (SandboxSessionState):
            desired_state (SandboxSessionDesiredState):
            region (str):
            memory_mb (int):
            created_at (datetime.datetime):
            expires_at (datetime.datetime | None): Absolute VM expiry. Null means unlimited in local mode.
            started_at (datetime.datetime | Unset):
     """

    id: UUID
    project_id: UUID
    sandbox_id: None | UUID
    state: SandboxSessionState
    desired_state: SandboxSessionDesiredState
    region: str
    memory_mb: int
    created_at: datetime.datetime
    expires_at: datetime.datetime | None
    started_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        sandbox_id: None | str
        if isinstance(self.sandbox_id, UUID):
            sandbox_id = str(self.sandbox_id)
        else:
            sandbox_id = self.sandbox_id

        state: str = self.state

        desired_state: str = self.desired_state

        region = self.region

        memory_mb = self.memory_mb

        created_at = self.created_at.isoformat()

        expires_at: None | str
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

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




        def _parse_sandbox_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                sandbox_id_type_0 = UUID(data)



                return sandbox_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        sandbox_id = _parse_sandbox_id(d.pop("sandbox_id"))


        state = check_sandbox_session_state(d.pop("state"))




        desired_state = check_sandbox_session_desired_state(d.pop("desired_state"))




        region = d.pop("region")

        memory_mb = d.pop("memory_mb")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        def _parse_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)



                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        expires_at = _parse_expires_at(d.pop("expires_at"))


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

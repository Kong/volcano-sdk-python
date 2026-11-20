from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sandbox_session_network_applied import check_sandbox_session_network_applied
from ..models.sandbox_session_network_applied import SandboxSessionNetworkApplied
from ..models.sandbox_session_network_egress import check_sandbox_session_network_egress
from ..models.sandbox_session_network_egress import SandboxSessionNetworkEgress
from typing import cast






T = TypeVar("T", bound="SandboxSessionNetwork")



@_attrs_define
class SandboxSessionNetwork:
    """
        Attributes:
            egress (SandboxSessionNetworkEgress): The outbound network policy the session was created with. It never
                changes.
            applied (SandboxSessionNetworkApplied): The outbound network policy Volcano last observed on the session's VM,
                never the request alone. It is `unknown` until the session is first observed, from a suspend or resume request
                until it is observed again, briefly while Volcano rolls out an update, and whenever the observation does not
                match the request. A terminated session keeps what Volcano last observed, so a `deny_all` session ended because
                Volcano observed outbound access reads `default`. A session first reports `state` `running` only once its
                network has been observed. To depend on `deny_all`, wait for `running`, then terminate the session unless
                `applied` is `deny_all`. Act on `applied` only while the session is `running`, and on a later `unknown` only
                while `desired_state` is `running`.
     """

    egress: SandboxSessionNetworkEgress
    applied: SandboxSessionNetworkApplied





    def to_dict(self) -> dict[str, Any]:
        egress: str = self.egress

        applied: str = self.applied


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "egress": egress,
            "applied": applied,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        egress = check_sandbox_session_network_egress(d.pop("egress"))




        applied = check_sandbox_session_network_applied(d.pop("applied"))




        sandbox_session_network = cls(
            egress=egress,
            applied=applied,
        )

        return sandbox_session_network

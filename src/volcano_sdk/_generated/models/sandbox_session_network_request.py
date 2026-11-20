from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.sandbox_session_network_request_egress import check_sandbox_session_network_request_egress
from ..models.sandbox_session_network_request_egress import SandboxSessionNetworkRequestEgress
from typing import cast






T = TypeVar("T", bound="SandboxSessionNetworkRequest")



@_attrs_define
class SandboxSessionNetworkRequest:
    """ Outbound network policy for the session. Omitting `network` is the same as `egress` `default`.

        Attributes:
            egress (SandboxSessionNetworkRequestEgress): `default` gives the session the region's standard outbound internet
                access. `deny_all` gives it no outbound network for its whole lifetime: DNS lookups, internet and link-local
                addresses, and connections back out through Volcano all fail, and the session accepts no port access. Commands,
                files and the rest of the session API work as usual. The policy cannot be changed after creation; suspend and
                resume keep it. Check `network.applied` before relying on it. Where `GET /capabilities` lists
                `sandboxes.network_isolation` as unavailable, `deny_all` answers `400` with code `feature_unavailable`.
     """

    egress: SandboxSessionNetworkRequestEgress





    def to_dict(self) -> dict[str, Any]:
        egress: str = self.egress


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "egress": egress,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        egress = check_sandbox_session_network_request_egress(d.pop("egress"))




        sandbox_session_network_request = cls(
            egress=egress,
        )

        return sandbox_session_network_request

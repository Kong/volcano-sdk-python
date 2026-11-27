from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LavaflowLineageEvidenceDeployment")



@_attrs_define
class LavaflowLineageEvidenceDeployment:
    """ 
        Attributes:
            commit_sha (str): The commit of the deployment that served the occurrence attribution judged (`opened_at`).
            commit_origin (str): `push` for a commit Volcano built from a push, `client_reported` for one the deploy client
                reported. New values may appear.
     """

    commit_sha: str
    commit_origin: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        commit_sha = self.commit_sha

        commit_origin = self.commit_origin


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "commit_sha": commit_sha,
            "commit_origin": commit_origin,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        commit_sha = d.pop("commit_sha")

        commit_origin = d.pop("commit_origin")

        lavaflow_lineage_evidence_deployment = cls(
            commit_sha=commit_sha,
            commit_origin=commit_origin,
        )


        lavaflow_lineage_evidence_deployment.additional_properties = d
        return lavaflow_lineage_evidence_deployment

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

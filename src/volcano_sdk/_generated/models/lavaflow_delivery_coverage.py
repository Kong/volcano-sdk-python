from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_delivery_coverage_state import check_lavaflow_delivery_coverage_state
from ..models.lavaflow_delivery_coverage_state import LavaflowDeliveryCoverageState
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="LavaflowDeliveryCoverage")



@_attrs_define
class LavaflowDeliveryCoverage:
    """ Another run's verified covering pull request. That run owns the pull request.

        Attributes:
            run_id (UUID):
            number (int):
            url (str):
            state (LavaflowDeliveryCoverageState):
            opened_at (datetime.datetime | None):
            merged_at (datetime.datetime | None):
            deployed_at (datetime.datetime | None):
            repository_id (int | Unset): Repository ID recorded for the pull request. Omitted if unknown.
     """

    run_id: UUID
    number: int
    url: str
    state: LavaflowDeliveryCoverageState
    opened_at: datetime.datetime | None
    merged_at: datetime.datetime | None
    deployed_at: datetime.datetime | None
    repository_id: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        run_id = str(self.run_id)

        number = self.number

        url = self.url

        state: str = self.state

        opened_at: None | str
        if isinstance(self.opened_at, datetime.datetime):
            opened_at = self.opened_at.isoformat()
        else:
            opened_at = self.opened_at

        merged_at: None | str
        if isinstance(self.merged_at, datetime.datetime):
            merged_at = self.merged_at.isoformat()
        else:
            merged_at = self.merged_at

        deployed_at: None | str
        if isinstance(self.deployed_at, datetime.datetime):
            deployed_at = self.deployed_at.isoformat()
        else:
            deployed_at = self.deployed_at

        repository_id = self.repository_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "run_id": run_id,
            "number": number,
            "url": url,
            "state": state,
            "opened_at": opened_at,
            "merged_at": merged_at,
            "deployed_at": deployed_at,
        })
        if repository_id is not UNSET:
            field_dict["repository_id"] = repository_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_id = UUID(d.pop("run_id"))




        number = d.pop("number")

        url = d.pop("url")

        state = check_lavaflow_delivery_coverage_state(d.pop("state"))




        def _parse_opened_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                opened_at_type_0 = datetime.datetime.fromisoformat(data)



                return opened_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        opened_at = _parse_opened_at(d.pop("opened_at"))


        def _parse_merged_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                merged_at_type_0 = datetime.datetime.fromisoformat(data)



                return merged_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        merged_at = _parse_merged_at(d.pop("merged_at"))


        def _parse_deployed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deployed_at_type_0 = datetime.datetime.fromisoformat(data)



                return deployed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        deployed_at = _parse_deployed_at(d.pop("deployed_at"))


        repository_id = d.pop("repository_id", UNSET)

        lavaflow_delivery_coverage = cls(
            run_id=run_id,
            number=number,
            url=url,
            state=state,
            opened_at=opened_at,
            merged_at=merged_at,
            deployed_at=deployed_at,
            repository_id=repository_id,
        )


        lavaflow_delivery_coverage.additional_properties = d
        return lavaflow_delivery_coverage

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

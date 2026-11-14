from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_production_environment_status import check_function_production_environment_status
from ..models.function_production_environment_status import FunctionProductionEnvironmentStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="FunctionProductionEnvironment")



@_attrs_define
class FunctionProductionEnvironment:
    """ Whether the function's own build has the project's current variables. While a preview serves the
    function, `volcano config deploy` and replacing the shared variable list skip the function, so its
    own build keeps the values it had. A rollback to the function's own build starts synchronizing them
    as it returns the traffic, and the status reads `current` once that synchronization completes or a
    deployment of the function activates. A synchronization that fails leaves it `out_of_date`.

        Attributes:
            status (FunctionProductionEnvironmentStatus): `out_of_date`: a stored variable change skipped the function while
                a preview served it.
            out_of_date_since (datetime.datetime | Unset): When the latest skipped change was stored. Absent while `status`
                is `current`.
     """

    status: FunctionProductionEnvironmentStatus
    out_of_date_since: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        out_of_date_since: str | Unset = UNSET
        if not isinstance(self.out_of_date_since, Unset):
            out_of_date_since = self.out_of_date_since.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
        })
        if out_of_date_since is not UNSET:
            field_dict["out_of_date_since"] = out_of_date_since

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_function_production_environment_status(d.pop("status"))




        _out_of_date_since = d.pop("out_of_date_since", UNSET)
        out_of_date_since: datetime.datetime | Unset
        if isinstance(_out_of_date_since,  Unset):
            out_of_date_since = UNSET
        else:
            out_of_date_since = datetime.datetime.fromisoformat(_out_of_date_since)




        function_production_environment = cls(
            status=status,
            out_of_date_since=out_of_date_since,
        )

        return function_production_environment


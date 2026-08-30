from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.database_stats_granularity import check_database_stats_granularity
from ..models.database_stats_granularity import DatabaseStatsGranularity
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.database_branch_storage import DatabaseBranchStorage





T = TypeVar("T", bound="DatabaseStats")



@_attrs_define
class DatabaseStats:
    """ 
        Attributes:
            current_storage_bytes (int): On-disk size right now, in bytes: the database itself, plus every
                branch's divergence from it, plus what its backups cost to hold. This
                is the figure the storage allowance is enforced against. `branches`
                and `backup_storage_bytes` break it down.
            current_storage_mb (float): `current_storage_bytes` expressed in megabytes.
            backup_storage_bytes (int): What this database's backups contribute to `current_storage_bytes`.

                A backup taken on request is charged as a full copy of the database
                as it was at that moment, so two backups of a 2 GB database are 4 GB.
                A backup schedule is charged its first snapshot in full and each
                later one only for the storage it adds. Deleting a backup releases
                its storage immediately.

                Sampled from the provider rather than measured live, so it can lag a
                change by a few minutes, and a backup taken seconds ago may not be
                costed yet. Zero on a plan without backups.
            storage_bytes (int): Total storage used in bytes (data + WAL)
            data_written_bytes (int): Total data written in bytes
            data_transfer_bytes (int): Total data transferred in bytes
            compute_time_seconds (float): Total CPU seconds consumed
            active_time_seconds (float): Total active compute time in seconds
            branches (list[DatabaseBranchStorage] | Unset): Per-branch contribution to `current_storage_bytes`. Empty when
                the
                database has no branches. A branch that has not diverged from its
                parent contributes nothing.
            time_range (str | Unset): Time range of the metrics (e.g., "2024-01-01T00:00:00Z to 2024-01-02T00:00:00Z")
            granularity (DatabaseStatsGranularity | Unset): Granularity of the aggregated metrics
     """

    current_storage_bytes: int
    current_storage_mb: float
    backup_storage_bytes: int
    storage_bytes: int
    data_written_bytes: int
    data_transfer_bytes: int
    compute_time_seconds: float
    active_time_seconds: float
    branches: list[DatabaseBranchStorage] | Unset = UNSET
    time_range: str | Unset = UNSET
    granularity: DatabaseStatsGranularity | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_branch_storage import DatabaseBranchStorage
        current_storage_bytes = self.current_storage_bytes

        current_storage_mb = self.current_storage_mb

        backup_storage_bytes = self.backup_storage_bytes

        storage_bytes = self.storage_bytes

        data_written_bytes = self.data_written_bytes

        data_transfer_bytes = self.data_transfer_bytes

        compute_time_seconds = self.compute_time_seconds

        active_time_seconds = self.active_time_seconds

        branches: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.branches, Unset):
            branches = []
            for branches_item_data in self.branches:
                branches_item = branches_item_data.to_dict()
                branches.append(branches_item)



        time_range = self.time_range

        granularity: str | Unset = UNSET
        if not isinstance(self.granularity, Unset):
            granularity = self.granularity



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "current_storage_bytes": current_storage_bytes,
            "current_storage_mb": current_storage_mb,
            "backup_storage_bytes": backup_storage_bytes,
            "storage_bytes": storage_bytes,
            "data_written_bytes": data_written_bytes,
            "data_transfer_bytes": data_transfer_bytes,
            "compute_time_seconds": compute_time_seconds,
            "active_time_seconds": active_time_seconds,
        })
        if branches is not UNSET:
            field_dict["branches"] = branches
        if time_range is not UNSET:
            field_dict["time_range"] = time_range
        if granularity is not UNSET:
            field_dict["granularity"] = granularity

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_branch_storage import DatabaseBranchStorage
        d = dict(src_dict)
        current_storage_bytes = d.pop("current_storage_bytes")

        current_storage_mb = d.pop("current_storage_mb")

        backup_storage_bytes = d.pop("backup_storage_bytes")

        storage_bytes = d.pop("storage_bytes")

        data_written_bytes = d.pop("data_written_bytes")

        data_transfer_bytes = d.pop("data_transfer_bytes")

        compute_time_seconds = d.pop("compute_time_seconds")

        active_time_seconds = d.pop("active_time_seconds")

        _branches = d.pop("branches", UNSET)
        branches: list[DatabaseBranchStorage] | Unset = UNSET
        if _branches is not UNSET:
            branches = []
            for branches_item_data in _branches:
                branches_item = DatabaseBranchStorage.from_dict(branches_item_data)



                branches.append(branches_item)


        time_range = d.pop("time_range", UNSET)

        _granularity = d.pop("granularity", UNSET)
        granularity: DatabaseStatsGranularity | Unset
        if isinstance(_granularity,  Unset):
            granularity = UNSET
        else:
            granularity = check_database_stats_granularity(_granularity)




        database_stats = cls(
            current_storage_bytes=current_storage_bytes,
            current_storage_mb=current_storage_mb,
            backup_storage_bytes=backup_storage_bytes,
            storage_bytes=storage_bytes,
            data_written_bytes=data_written_bytes,
            data_transfer_bytes=data_transfer_bytes,
            compute_time_seconds=compute_time_seconds,
            active_time_seconds=active_time_seconds,
            branches=branches,
            time_range=time_range,
            granularity=granularity,
        )


        database_stats.additional_properties = d
        return database_stats

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

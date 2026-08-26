from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.database_query_performance_database import DatabaseQueryPerformanceDatabase





T = TypeVar("T", bound="DatabaseQueryPerformanceItem")



@_attrs_define
class DatabaseQueryPerformanceItem:
    """ 
        Attributes:
            query_id (str): pg_stat_statements query identifier.
            query (str): Normalized and obfuscated representative query text.
            database (DatabaseQueryPerformanceDatabase):
            role (str): Database role used for the query.
            calls (int):
            total_exec_time_seconds (float): Cumulative total execution time from pg_stat_statements in seconds.
            max_exec_time_seconds (float):
            mean_exec_time_seconds (float):
            min_exec_time_seconds (float):
            rows_processed (int):
     """

    query_id: str
    query: str
    database: DatabaseQueryPerformanceDatabase
    role: str
    calls: int
    total_exec_time_seconds: float
    max_exec_time_seconds: float
    mean_exec_time_seconds: float
    min_exec_time_seconds: float
    rows_processed: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.database_query_performance_database import DatabaseQueryPerformanceDatabase
        query_id = self.query_id

        query = self.query

        database = self.database.to_dict()

        role = self.role

        calls = self.calls

        total_exec_time_seconds = self.total_exec_time_seconds

        max_exec_time_seconds = self.max_exec_time_seconds

        mean_exec_time_seconds = self.mean_exec_time_seconds

        min_exec_time_seconds = self.min_exec_time_seconds

        rows_processed = self.rows_processed


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "query_id": query_id,
            "query": query,
            "database": database,
            "role": role,
            "calls": calls,
            "total_exec_time_seconds": total_exec_time_seconds,
            "max_exec_time_seconds": max_exec_time_seconds,
            "mean_exec_time_seconds": mean_exec_time_seconds,
            "min_exec_time_seconds": min_exec_time_seconds,
            "rows_processed": rows_processed,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.database_query_performance_database import DatabaseQueryPerformanceDatabase
        d = dict(src_dict)
        query_id = d.pop("query_id")

        query = d.pop("query")

        database = DatabaseQueryPerformanceDatabase.from_dict(d.pop("database"))




        role = d.pop("role")

        calls = d.pop("calls")

        total_exec_time_seconds = d.pop("total_exec_time_seconds")

        max_exec_time_seconds = d.pop("max_exec_time_seconds")

        mean_exec_time_seconds = d.pop("mean_exec_time_seconds")

        min_exec_time_seconds = d.pop("min_exec_time_seconds")

        rows_processed = d.pop("rows_processed")

        database_query_performance_item = cls(
            query_id=query_id,
            query=query,
            database=database,
            role=role,
            calls=calls,
            total_exec_time_seconds=total_exec_time_seconds,
            max_exec_time_seconds=max_exec_time_seconds,
            mean_exec_time_seconds=mean_exec_time_seconds,
            min_exec_time_seconds=min_exec_time_seconds,
            rows_processed=rows_processed,
        )


        database_query_performance_item.additional_properties = d
        return database_query_performance_item

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.resource_reference import ResourceReference





T = TypeVar("T", bound="GitDeploymentMigrationRun")



@_attrs_define
class GitDeploymentMigrationRun:
    """ A migration run a deployment run started. Get it at `GET /projects/{id}/databases/{databaseName}/migration-
    runs/{runId}` with `database.name` and `id`.

        Attributes:
            id (UUID):
            database (ResourceReference): Stable reference to a Volcano resource.
     """

    id: UUID
    database: ResourceReference
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_reference import ResourceReference # noqa: PLC0415
        id = str(self.id)

        database = self.database.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "database": database,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_reference import ResourceReference # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        database = ResourceReference.from_dict(d.pop("database"))




        git_deployment_migration_run = cls(
            id=id,
            database=database,
        )


        git_deployment_migration_run.additional_properties = d
        return git_deployment_migration_run

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

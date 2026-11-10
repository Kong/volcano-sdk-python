from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_template_installation_phase import check_project_template_installation_phase
from ..models.project_template_installation_phase import ProjectTemplateInstallationPhase
from ..models.project_template_installation_status import check_project_template_installation_status
from ..models.project_template_installation_status import ProjectTemplateInstallationStatus
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_template_installation_source import ProjectTemplateInstallationSource





T = TypeVar("T", bound="ProjectTemplateInstallation")



@_attrs_define
class ProjectTemplateInstallation:
    """ Template initialization progress, returned by project creation and the
    individual project endpoint. Omitted for projects without a template.
    Project creation accepts the installation; wait for `ready` before use.
    A failed installation retains the project for inspection or deletion.

        Attributes:
            status (ProjectTemplateInstallationStatus):
            phase (ProjectTemplateInstallationPhase):
            source (ProjectTemplateInstallationSource | Unset): The share release a fork was installed from.
            failure_code (str | Unset): Why the installation failed. Present only when `status` is `failed`, and
                absent for installations that failed before Volcano recorded a reason.
                New codes can be added, so treat an unknown one as a generic failure.
                `source_withdrawn`: the deploy link was switched off or deleted, or its
                project is being deleted. `source_invalid`: the source failed Volcano's checks,
                such as a release archive whose digest, size or contents are wrong.
                `source_access_lost`: Volcano can no longer read the source repository.
                `invalid_source_configuration`: the source's `volcano-config.yaml` is
                invalid, or it declares a variable the new project does not have.
                `nothing_to_deploy`: the source has no function or frontend.
                `database_not_supported`: the source ships database SQL.
                `function_deploy_refused`: a function in the source cannot be deployed
                as defined. `function_quota_exceeded`,
                `durable_function_quota_exceeded`, `frontend_quota_exceeded`,
                `frontend_deploy_limit` and `build_minutes_exceeded`: the project
                reached a plan limit. `build_failed`: a function or frontend from the
                source failed to build or deploy; its deployment's build logs say why.
                `retry_budget_exhausted`: the installation kept failing and Volcano
                stopped retrying. `internal_error`: Volcano failed for a reason of its
                own.
                 Example: source_withdrawn.
     """

    status: ProjectTemplateInstallationStatus
    phase: ProjectTemplateInstallationPhase
    source: ProjectTemplateInstallationSource | Unset = UNSET
    failure_code: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_template_installation_source import ProjectTemplateInstallationSource # noqa: PLC0415
        status: str = self.status

        phase: str = self.phase

        source: dict[str, Any] | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        failure_code = self.failure_code


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "phase": phase,
        })
        if source is not UNSET:
            field_dict["source"] = source
        if failure_code is not UNSET:
            field_dict["failure_code"] = failure_code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_template_installation_source import ProjectTemplateInstallationSource # noqa: PLC0415
        d = dict(src_dict)
        status = check_project_template_installation_status(d.pop("status"))




        phase = check_project_template_installation_phase(d.pop("phase"))




        _source = d.pop("source", UNSET)
        source: ProjectTemplateInstallationSource | Unset
        if isinstance(_source,  Unset):
            source = UNSET
        else:
            source = ProjectTemplateInstallationSource.from_dict(_source)




        failure_code = d.pop("failure_code", UNSET)

        project_template_installation = cls(
            status=status,
            phase=phase,
            source=source,
            failure_code=failure_code,
        )


        project_template_installation.additional_properties = d
        return project_template_installation

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

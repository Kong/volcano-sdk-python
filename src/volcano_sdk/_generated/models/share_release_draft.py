from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.share_release_draft_frontend_variables import ShareReleaseDraftFrontendVariables
  from ..models.share_release_function import ShareReleaseFunction
  from ..models.share_release_omission import ShareReleaseOmission
  from ..models.share_variable import ShareVariable





T = TypeVar("T", bound="ShareReleaseDraft")



@_attrs_define
class ShareReleaseDraft:
    """ 
        Attributes:
            draft_id (str): Opaque. Names exactly what a release built now would carry: each
                function's and frontend's current deployment, and everything the draft
                lists, including each function's settings (`http_auth_mode`,
                `openapi_spec_sha256`, `variable_scope`), the `variables`, the
                `frontend_variables` and the `omissions`. It stays the same while those
                do, and changes when a function or frontend is redeployed or anything the
                draft lists changes. A sandbox is not part of it, since a release does not
                carry one: rebuilding only a sandbox leaves it unchanged. Send it with the
                publish.
            functions (list[ShareReleaseFunction]):
            frontends (list[str]):
            variables (list[ShareVariable]): The project's variables a visitor could be asked to supply. Volcano's own, such
                as `VOLCANO_API_URL`, are never listed.
            service_key_functions (list[str]): The functions whose code reads `VOLCANO_SERVICE_KEY`. A release gives them
                the visitor project's service key once the owner confirms them.
            omissions (list[ShareReleaseOmission]):
            frontend_variables (ShareReleaseDraftFrontendVariables): The draft's variables each frontend receives, by
                frontend name, as your
                project's frontend of that name selects them by its variable scope now.
                A frontend receives no others.
     """

    draft_id: str
    functions: list[ShareReleaseFunction]
    frontends: list[str]
    variables: list[ShareVariable]
    service_key_functions: list[str]
    omissions: list[ShareReleaseOmission]
    frontend_variables: ShareReleaseDraftFrontendVariables
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.share_release_draft_frontend_variables import ShareReleaseDraftFrontendVariables # noqa: PLC0415
        from ..models.share_release_function import ShareReleaseFunction # noqa: PLC0415
        from ..models.share_release_omission import ShareReleaseOmission # noqa: PLC0415
        from ..models.share_variable import ShareVariable # noqa: PLC0415
        draft_id = self.draft_id

        functions = []
        for functions_item_data in self.functions:
            functions_item = functions_item_data.to_dict()
            functions.append(functions_item)



        frontends = self.frontends



        variables = []
        for variables_item_data in self.variables:
            variables_item = variables_item_data.to_dict()
            variables.append(variables_item)



        service_key_functions = self.service_key_functions



        omissions = []
        for omissions_item_data in self.omissions:
            omissions_item = omissions_item_data.to_dict()
            omissions.append(omissions_item)



        frontend_variables = self.frontend_variables.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "draft_id": draft_id,
            "functions": functions,
            "frontends": frontends,
            "variables": variables,
            "service_key_functions": service_key_functions,
            "omissions": omissions,
            "frontend_variables": frontend_variables,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.share_release_draft_frontend_variables import ShareReleaseDraftFrontendVariables # noqa: PLC0415
        from ..models.share_release_function import ShareReleaseFunction # noqa: PLC0415
        from ..models.share_release_omission import ShareReleaseOmission # noqa: PLC0415
        from ..models.share_variable import ShareVariable # noqa: PLC0415
        d = dict(src_dict)
        draft_id = d.pop("draft_id")

        functions = []
        _functions = d.pop("functions")
        for functions_item_data in (_functions):
            functions_item = ShareReleaseFunction.from_dict(functions_item_data)



            functions.append(functions_item)


        frontends = cast(list[str], d.pop("frontends"))


        variables = []
        _variables = d.pop("variables")
        for variables_item_data in (_variables):
            variables_item = ShareVariable.from_dict(variables_item_data)



            variables.append(variables_item)


        service_key_functions = cast(list[str], d.pop("service_key_functions"))


        omissions = []
        _omissions = d.pop("omissions")
        for omissions_item_data in (_omissions):
            omissions_item = ShareReleaseOmission.from_dict(omissions_item_data)



            omissions.append(omissions_item)


        frontend_variables = ShareReleaseDraftFrontendVariables.from_dict(d.pop("frontend_variables"))




        share_release_draft = cls(
            draft_id=draft_id,
            functions=functions,
            frontends=frontends,
            variables=variables,
            service_key_functions=service_key_functions,
            omissions=omissions,
            frontend_variables=frontend_variables,
        )


        share_release_draft.additional_properties = d
        return share_release_draft

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

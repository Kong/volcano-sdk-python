from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.share_release_function_kind import check_share_release_function_kind
from ..models.share_release_function_kind import ShareReleaseFunctionKind
from ..models.share_release_function_variable_scope import check_share_release_function_variable_scope
from ..models.share_release_function_variable_scope import ShareReleaseFunctionVariableScope
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ShareReleaseFunction")



@_attrs_define
class ShareReleaseFunction:
    """ 
        Attributes:
            name (str):
            kind (ShareReleaseFunctionKind):
            visibility (str | Unset): The function's invocation visibility, as installed.
            invocation_mode (str | Unset): The function's invocation mode, when it is not the default.
            http_auth_mode (str | Unset): How the function's HTTP invocations authenticate, when its invocation
                settings are not the default; omitted means `volcano`. `none` lets
                anyone call the function without a credential in every project made from
                the release. Releases published before this was recorded omit it.
            openapi_spec_sha256 (str | Unset): The SHA-256 of the function's OpenAPI document as the release carries it,
                when it has one, so a draft shows when the document changed. Releases
                published before this was recorded omit it.
            variable_scope (ShareReleaseFunctionVariableScope | Unset): `scoped` when the function receives only the
                variables it declares, as
                your project's function does, listed in `variables`. Omitted when it
                receives every variable shared with functions. The service key is not
                part of it: `service_key_functions` says which functions receive that.
                Releases published before this was recorded omit it.
            variables (list[str] | Unset): For a `scoped` function, the variables it declares that a project made from the
                release has.
     """

    name: str
    kind: ShareReleaseFunctionKind
    visibility: str | Unset = UNSET
    invocation_mode: str | Unset = UNSET
    http_auth_mode: str | Unset = UNSET
    openapi_spec_sha256: str | Unset = UNSET
    variable_scope: ShareReleaseFunctionVariableScope | Unset = UNSET
    variables: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        kind: str = self.kind

        visibility = self.visibility

        invocation_mode = self.invocation_mode

        http_auth_mode = self.http_auth_mode

        openapi_spec_sha256 = self.openapi_spec_sha256

        variable_scope: str | Unset = UNSET
        if not isinstance(self.variable_scope, Unset):
            variable_scope = self.variable_scope


        variables: list[str] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "kind": kind,
        })
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if invocation_mode is not UNSET:
            field_dict["invocation_mode"] = invocation_mode
        if http_auth_mode is not UNSET:
            field_dict["http_auth_mode"] = http_auth_mode
        if openapi_spec_sha256 is not UNSET:
            field_dict["openapi_spec_sha256"] = openapi_spec_sha256
        if variable_scope is not UNSET:
            field_dict["variable_scope"] = variable_scope
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        kind = check_share_release_function_kind(d.pop("kind"))




        visibility = d.pop("visibility", UNSET)

        invocation_mode = d.pop("invocation_mode", UNSET)

        http_auth_mode = d.pop("http_auth_mode", UNSET)

        openapi_spec_sha256 = d.pop("openapi_spec_sha256", UNSET)

        _variable_scope = d.pop("variable_scope", UNSET)
        variable_scope: ShareReleaseFunctionVariableScope | Unset
        if isinstance(_variable_scope,  Unset):
            variable_scope = UNSET
        else:
            variable_scope = check_share_release_function_variable_scope(_variable_scope)




        variables = cast(list[str], d.pop("variables", UNSET))


        share_release_function = cls(
            name=name,
            kind=kind,
            visibility=visibility,
            invocation_mode=invocation_mode,
            http_auth_mode=http_auth_mode,
            openapi_spec_sha256=openapi_spec_sha256,
            variable_scope=variable_scope,
            variables=variables,
        )


        share_release_function.additional_properties = d
        return share_release_function

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

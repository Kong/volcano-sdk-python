from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_http_auth_mode import check_function_http_auth_mode
from ..models.function_http_auth_mode import FunctionHTTPAuthMode
from ..models.function_invocation_mode import check_function_invocation_mode
from ..models.function_invocation_mode import FunctionInvocationMode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_function_openapi_spec_type_0 import ProjectConfigFunctionOpenapiSpecType0
  from ..models.project_config_scheduler import ProjectConfigScheduler





T = TypeVar("T", bound="ProjectConfigFunction")



@_attrs_define
class ProjectConfigFunction:
    """ Configuration for an existing (deployed) function. Functions are never
    created or deleted through the manifest. When `schedulers` is declared
    it is fully synced (schedulers absent from the list are deleted);
    omitting `schedulers` leaves the function's schedulers untouched.

        Attributes:
            name (str):
            public (bool | Unset): Function visibility for anon-key invocation
            invocation_mode (FunctionInvocationMode | Unset): Invocation contract. `rpc` preserves the existing POST
                `{payload: ...}` contract;
                `http` forwards HTTP request semantics to the function runtime.
            http_auth_mode (FunctionHTTPAuthMode | Unset): Authentication applied by the HTTP ingress. `none` is valid only
                for public
                HTTP-mode functions and is intended for externally signed webhooks.
            openapi_spec (None | ProjectConfigFunctionOpenapiSpecType0 | Unset): OpenAPI 3.0 or 3.1 metadata for an HTTP-
                mode function
            schedulers (list[ProjectConfigScheduler] | Unset):
     """

    name: str
    public: bool | Unset = UNSET
    invocation_mode: FunctionInvocationMode | Unset = UNSET
    http_auth_mode: FunctionHTTPAuthMode | Unset = UNSET
    openapi_spec: None | ProjectConfigFunctionOpenapiSpecType0 | Unset = UNSET
    schedulers: list[ProjectConfigScheduler] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_function_openapi_spec_type_0 import ProjectConfigFunctionOpenapiSpecType0
        from ..models.project_config_scheduler import ProjectConfigScheduler
        name = self.name

        public = self.public

        invocation_mode: str | Unset = UNSET
        if not isinstance(self.invocation_mode, Unset):
            invocation_mode = self.invocation_mode


        http_auth_mode: str | Unset = UNSET
        if not isinstance(self.http_auth_mode, Unset):
            http_auth_mode = self.http_auth_mode


        openapi_spec: dict[str, Any] | None | Unset
        if isinstance(self.openapi_spec, Unset):
            openapi_spec = UNSET
        elif isinstance(self.openapi_spec, ProjectConfigFunctionOpenapiSpecType0):
            openapi_spec = self.openapi_spec.to_dict()
        else:
            openapi_spec = self.openapi_spec

        schedulers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.schedulers, Unset):
            schedulers = []
            for schedulers_item_data in self.schedulers:
                schedulers_item = schedulers_item_data.to_dict()
                schedulers.append(schedulers_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if public is not UNSET:
            field_dict["public"] = public
        if invocation_mode is not UNSET:
            field_dict["invocation_mode"] = invocation_mode
        if http_auth_mode is not UNSET:
            field_dict["http_auth_mode"] = http_auth_mode
        if openapi_spec is not UNSET:
            field_dict["openapi_spec"] = openapi_spec
        if schedulers is not UNSET:
            field_dict["schedulers"] = schedulers

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_function_openapi_spec_type_0 import ProjectConfigFunctionOpenapiSpecType0
        from ..models.project_config_scheduler import ProjectConfigScheduler
        d = dict(src_dict)
        name = d.pop("name")

        public = d.pop("public", UNSET)

        _invocation_mode = d.pop("invocation_mode", UNSET)
        invocation_mode: FunctionInvocationMode | Unset
        if isinstance(_invocation_mode,  Unset):
            invocation_mode = UNSET
        else:
            invocation_mode = check_function_invocation_mode(_invocation_mode)




        _http_auth_mode = d.pop("http_auth_mode", UNSET)
        http_auth_mode: FunctionHTTPAuthMode | Unset
        if isinstance(_http_auth_mode,  Unset):
            http_auth_mode = UNSET
        else:
            http_auth_mode = check_function_http_auth_mode(_http_auth_mode)




        def _parse_openapi_spec(data: object) -> None | ProjectConfigFunctionOpenapiSpecType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                openapi_spec_type_0 = ProjectConfigFunctionOpenapiSpecType0.from_dict(data)



                return openapi_spec_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProjectConfigFunctionOpenapiSpecType0 | Unset, data)

        openapi_spec = _parse_openapi_spec(d.pop("openapi_spec", UNSET))


        _schedulers = d.pop("schedulers", UNSET)
        schedulers: list[ProjectConfigScheduler] | Unset = UNSET
        if _schedulers is not UNSET:
            schedulers = []
            for schedulers_item_data in _schedulers:
                schedulers_item = ProjectConfigScheduler.from_dict(schedulers_item_data)



                schedulers.append(schedulers_item)


        project_config_function = cls(
            name=name,
            public=public,
            invocation_mode=invocation_mode,
            http_auth_mode=http_auth_mode,
            openapi_spec=openapi_spec,
            schedulers=schedulers,
        )

        return project_config_function


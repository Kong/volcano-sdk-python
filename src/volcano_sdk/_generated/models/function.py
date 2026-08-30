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
from ..models.function_status import check_function_status
from ..models.function_status import FunctionStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.function_openapi_spec_type_0 import FunctionOpenapiSpecType0





T = TypeVar("T", bound="Function")



@_attrs_define
class Function:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            name (str):
            status (FunctionStatus):
            is_public (bool): Function visibility for anon-key invocation.
                - `false` (default): only auth user tokens and service keys can invoke
                - `true`: anon keys with `functions.invoke` can invoke
            invocation_mode (FunctionInvocationMode): Invocation contract. `rpc` preserves the existing POST `{payload:
                ...}` contract;
                `http` forwards HTTP request semantics to the function runtime. A function with a custom
                domain attached or detaching cannot switch from `http` to `rpc` until detachment completes.
            http_auth_mode (FunctionHTTPAuthMode): Authentication applied by the HTTP ingress. `none` is valid only for
                public
                HTTP-mode functions and is intended for externally signed webhooks.
            openapi_spec (FunctionOpenapiSpecType0 | None): Optional OpenAPI 3.0 or 3.1 document describing an HTTP-mode
                function.
            has_openapi_spec (bool): Whether OpenAPI metadata is configured; list responses omit the document itself.
            deployed_regions (list[str]): Regions where this function is currently deployed
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            provisioning_started_at (datetime.datetime | Unset): Timestamp when the current provisioning phase started
            aws_function_arn (str | Unset):
            invoke_url (str | Unset): Canonical GeoDNS endpoint URL for invoking this function (always HTTPS)
            runtime (str | Unset):
            handler (str | Unset):
            current_deployment_id (UUID | Unset): Identifier of the latest function deployment operation
            pending_deployment_id (UUID | Unset): Newest queued deployment that will run after the current operation
            last_invoked_at (datetime.datetime | Unset): Most recent successful invocation timestamp
     """

    id: UUID
    project_id: UUID
    name: str
    status: FunctionStatus
    is_public: bool
    invocation_mode: FunctionInvocationMode
    http_auth_mode: FunctionHTTPAuthMode
    openapi_spec: FunctionOpenapiSpecType0 | None
    has_openapi_spec: bool
    deployed_regions: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    provisioning_started_at: datetime.datetime | Unset = UNSET
    aws_function_arn: str | Unset = UNSET
    invoke_url: str | Unset = UNSET
    runtime: str | Unset = UNSET
    handler: str | Unset = UNSET
    current_deployment_id: UUID | Unset = UNSET
    pending_deployment_id: UUID | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.function_openapi_spec_type_0 import FunctionOpenapiSpecType0
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        status: str = self.status

        is_public = self.is_public

        invocation_mode: str = self.invocation_mode

        http_auth_mode: str = self.http_auth_mode

        openapi_spec: dict[str, Any] | None
        if isinstance(self.openapi_spec, FunctionOpenapiSpecType0):
            openapi_spec = self.openapi_spec.to_dict()
        else:
            openapi_spec = self.openapi_spec

        has_openapi_spec = self.has_openapi_spec

        deployed_regions = self.deployed_regions



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        provisioning_started_at: str | Unset = UNSET
        if not isinstance(self.provisioning_started_at, Unset):
            provisioning_started_at = self.provisioning_started_at.isoformat()

        aws_function_arn = self.aws_function_arn

        invoke_url = self.invoke_url

        runtime = self.runtime

        handler = self.handler

        current_deployment_id: str | Unset = UNSET
        if not isinstance(self.current_deployment_id, Unset):
            current_deployment_id = str(self.current_deployment_id)

        pending_deployment_id: str | Unset = UNSET
        if not isinstance(self.pending_deployment_id, Unset):
            pending_deployment_id = str(self.pending_deployment_id)

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "status": status,
            "is_public": is_public,
            "invocation_mode": invocation_mode,
            "http_auth_mode": http_auth_mode,
            "openapi_spec": openapi_spec,
            "has_openapi_spec": has_openapi_spec,
            "deployed_regions": deployed_regions,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if provisioning_started_at is not UNSET:
            field_dict["provisioning_started_at"] = provisioning_started_at
        if aws_function_arn is not UNSET:
            field_dict["aws_function_arn"] = aws_function_arn
        if invoke_url is not UNSET:
            field_dict["invoke_url"] = invoke_url
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if handler is not UNSET:
            field_dict["handler"] = handler
        if current_deployment_id is not UNSET:
            field_dict["current_deployment_id"] = current_deployment_id
        if pending_deployment_id is not UNSET:
            field_dict["pending_deployment_id"] = pending_deployment_id
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_openapi_spec_type_0 import FunctionOpenapiSpecType0
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        status = check_function_status(d.pop("status"))




        is_public = d.pop("is_public")

        invocation_mode = check_function_invocation_mode(d.pop("invocation_mode"))




        http_auth_mode = check_function_http_auth_mode(d.pop("http_auth_mode"))




        def _parse_openapi_spec(data: object) -> FunctionOpenapiSpecType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                openapi_spec_type_0 = FunctionOpenapiSpecType0.from_dict(data)



                return openapi_spec_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FunctionOpenapiSpecType0 | None, data)

        openapi_spec = _parse_openapi_spec(d.pop("openapi_spec"))


        has_openapi_spec = d.pop("has_openapi_spec")

        deployed_regions = cast(list[str], d.pop("deployed_regions"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _provisioning_started_at = d.pop("provisioning_started_at", UNSET)
        provisioning_started_at: datetime.datetime | Unset
        if isinstance(_provisioning_started_at,  Unset):
            provisioning_started_at = UNSET
        else:
            provisioning_started_at = datetime.datetime.fromisoformat(_provisioning_started_at)




        aws_function_arn = d.pop("aws_function_arn", UNSET)

        invoke_url = d.pop("invoke_url", UNSET)

        runtime = d.pop("runtime", UNSET)

        handler = d.pop("handler", UNSET)

        _current_deployment_id = d.pop("current_deployment_id", UNSET)
        current_deployment_id: UUID | Unset
        if isinstance(_current_deployment_id,  Unset):
            current_deployment_id = UNSET
        else:
            current_deployment_id = UUID(_current_deployment_id)




        _pending_deployment_id = d.pop("pending_deployment_id", UNSET)
        pending_deployment_id: UUID | Unset
        if isinstance(_pending_deployment_id,  Unset):
            pending_deployment_id = UNSET
        else:
            pending_deployment_id = UUID(_pending_deployment_id)




        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        function = cls(
            id=id,
            project_id=project_id,
            name=name,
            status=status,
            is_public=is_public,
            invocation_mode=invocation_mode,
            http_auth_mode=http_auth_mode,
            openapi_spec=openapi_spec,
            has_openapi_spec=has_openapi_spec,
            deployed_regions=deployed_regions,
            created_at=created_at,
            updated_at=updated_at,
            provisioning_started_at=provisioning_started_at,
            aws_function_arn=aws_function_arn,
            invoke_url=invoke_url,
            runtime=runtime,
            handler=handler,
            current_deployment_id=current_deployment_id,
            pending_deployment_id=pending_deployment_id,
            last_invoked_at=last_invoked_at,
        )


        function.additional_properties = d
        return function

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

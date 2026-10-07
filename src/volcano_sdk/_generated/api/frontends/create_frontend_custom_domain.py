from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_frontend_custom_domain_request import CreateFrontendCustomDomainRequest
from ...models.error import Error
from ...models.frontend_custom_domain_conflict_error import FrontendCustomDomainConflictError
from ...models.frontend_custom_domain_response import FrontendCustomDomainResponse
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    body: CreateFrontendCustomDomainRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/domain".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse | None:
    if response.status_code == 200:
        response_200 = FrontendCustomDomainResponse.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = FrontendCustomDomainResponse.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = FrontendCustomDomainConflictError.from_dict(response.json())



        return response_409

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendCustomDomainRequest,

) -> Response[Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse]:
    """ Configure frontend custom domain (SUPERAGENT)

     Configures one custom domain for a frontend.
    The default Volcano-generated frontend URL remains active.
    Wildcard Volcano frontend TLS remains valid and isolated from custom-domain certificate changes.
    The account must own the hostname: it must have verified the hostname or a domain above it (see
    `POST /user/domains`). A certificate does not prove ownership.
    When the account owns no domain covering the hostname, Volcano asks for a TXT record at
    `_volcano.<registrable domain>`, such as `_volcano.example.com`. Publishing it verifies the whole
    domain, so later subdomains need no record. A managed TLS request reserves the hostname and returns
    that record in `verification_records`; the reservation expires after 72 hours unless the record is
    published. A BYOC request gets `409` with `code: ownership_verification_required` and the record in
    `required_record`; publish it and send the same request again.
    Managed TLS then returns the CNAME that authorizes certificate issuance and renewal.
    An unverified reservation does not block an account that proves ownership. When another account
    holds one, a request gets `409` with `code: ownership_verification_required` and the caller's own
    `required_record`; after publishing it, the same request takes over the reservation. When another
    account verified the domain, the same `409` names the record that moves the domain to the caller
    once the other account's record is no longer published. A hostname below a domain another account
    owns otherwise returns `409` without `code`.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendCustomDomainRequest,

) -> Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse | None:
    """ Configure frontend custom domain (SUPERAGENT)

     Configures one custom domain for a frontend.
    The default Volcano-generated frontend URL remains active.
    Wildcard Volcano frontend TLS remains valid and isolated from custom-domain certificate changes.
    The account must own the hostname: it must have verified the hostname or a domain above it (see
    `POST /user/domains`). A certificate does not prove ownership.
    When the account owns no domain covering the hostname, Volcano asks for a TXT record at
    `_volcano.<registrable domain>`, such as `_volcano.example.com`. Publishing it verifies the whole
    domain, so later subdomains need no record. A managed TLS request reserves the hostname and returns
    that record in `verification_records`; the reservation expires after 72 hours unless the record is
    published. A BYOC request gets `409` with `code: ownership_verification_required` and the record in
    `required_record`; publish it and send the same request again.
    Managed TLS then returns the CNAME that authorizes certificate issuance and renewal.
    An unverified reservation does not block an account that proves ownership. When another account
    holds one, a request gets `409` with `code: ownership_verification_required` and the caller's own
    `required_record`; after publishing it, the same request takes over the reservation. When another
    account verified the domain, the same `409` names the record that moves the domain to the caller
    once the other account's record is no longer published. A hostname below a domain another account
    owns otherwise returns `409` without `code`.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendCustomDomainRequest,

) -> Response[Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse]:
    """ Configure frontend custom domain (SUPERAGENT)

     Configures one custom domain for a frontend.
    The default Volcano-generated frontend URL remains active.
    Wildcard Volcano frontend TLS remains valid and isolated from custom-domain certificate changes.
    The account must own the hostname: it must have verified the hostname or a domain above it (see
    `POST /user/domains`). A certificate does not prove ownership.
    When the account owns no domain covering the hostname, Volcano asks for a TXT record at
    `_volcano.<registrable domain>`, such as `_volcano.example.com`. Publishing it verifies the whole
    domain, so later subdomains need no record. A managed TLS request reserves the hostname and returns
    that record in `verification_records`; the reservation expires after 72 hours unless the record is
    published. A BYOC request gets `409` with `code: ownership_verification_required` and the record in
    `required_record`; publish it and send the same request again.
    Managed TLS then returns the CNAME that authorizes certificate issuance and renewal.
    An unverified reservation does not block an account that proves ownership. When another account
    holds one, a request gets `409` with `code: ownership_verification_required` and the caller's own
    `required_record`; after publishing it, the same request takes over the reservation. When another
    account verified the domain, the same `409` names the record that moves the domain to the caller
    once the other account's record is no longer published. A hostname below a domain another account
    owns otherwise returns `409` without `code`.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendCustomDomainRequest,

) -> Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse | None:
    """ Configure frontend custom domain (SUPERAGENT)

     Configures one custom domain for a frontend.
    The default Volcano-generated frontend URL remains active.
    Wildcard Volcano frontend TLS remains valid and isolated from custom-domain certificate changes.
    The account must own the hostname: it must have verified the hostname or a domain above it (see
    `POST /user/domains`). A certificate does not prove ownership.
    When the account owns no domain covering the hostname, Volcano asks for a TXT record at
    `_volcano.<registrable domain>`, such as `_volcano.example.com`. Publishing it verifies the whole
    domain, so later subdomains need no record. A managed TLS request reserves the hostname and returns
    that record in `verification_records`; the reservation expires after 72 hours unless the record is
    published. A BYOC request gets `409` with `code: ownership_verification_required` and the record in
    `required_record`; publish it and send the same request again.
    Managed TLS then returns the CNAME that authorizes certificate issuance and renewal.
    An unverified reservation does not block an account that proves ownership. When another account
    holds one, a request gets `409` with `code: ownership_verification_required` and the caller's own
    `required_record`; after publishing it, the same request takes over the reservation. When another
    account verified the domain, the same `409` names the record that moves the domain to the caller
    once the other account's record is no longer published. A hostname below a domain another account
    owns otherwise returns `409` without `code`.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    )).parsed

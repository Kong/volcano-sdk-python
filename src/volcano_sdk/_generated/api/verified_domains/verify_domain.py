from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.frontend_custom_domain_conflict_error import FrontendCustomDomainConflictError
from ...models.verified_domain import VerifiedDomain
from ...models.verify_domain_request import VerifyDomainRequest
from typing import cast



def request_kwargs(
    *,
    body: VerifyDomainRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user/domains",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendCustomDomainConflictError | VerifiedDomain | None:
    if response.status_code == 200:
        response_200 = VerifiedDomain.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = VerifiedDomain.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 409:
        response_409 = FrontendCustomDomainConflictError.from_dict(response.json())



        return response_409

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendCustomDomainConflictError | VerifiedDomain]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: VerifyDomainRequest,

) -> Response[Error | FrontendCustomDomainConflictError | VerifiedDomain]:
    """ Verify a domain

     Verifies the account's ownership of a domain and every name below it.
    Verify a registrable domain such as `example.com` to cover all of its
    subdomains, or a delegated subdomain you control.

    Publish a TXT record named `_volcano.<domain>`, then send this request.
    Without the record, the response is `409` with
    `code: ownership_verification_required` and the `required_record` to
    publish. Its value is the same on every request. The record must be
    served at that name itself; a record reached through a CNAME does not
    count.

    When another account verified the domain, publishing your record moves
    the domain to your account once that account's record is no longer
    published. Keep your record published so the domain stays yours.

    Verifying a domain the account already verified returns `200`.

    Args:
        body (VerifyDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCustomDomainConflictError | VerifiedDomain]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: VerifyDomainRequest,

) -> Error | FrontendCustomDomainConflictError | VerifiedDomain | None:
    """ Verify a domain

     Verifies the account's ownership of a domain and every name below it.
    Verify a registrable domain such as `example.com` to cover all of its
    subdomains, or a delegated subdomain you control.

    Publish a TXT record named `_volcano.<domain>`, then send this request.
    Without the record, the response is `409` with
    `code: ownership_verification_required` and the `required_record` to
    publish. Its value is the same on every request. The record must be
    served at that name itself; a record reached through a CNAME does not
    count.

    When another account verified the domain, publishing your record moves
    the domain to your account once that account's record is no longer
    published. Keep your record published so the domain stays yours.

    Verifying a domain the account already verified returns `200`.

    Args:
        body (VerifyDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCustomDomainConflictError | VerifiedDomain
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: VerifyDomainRequest,

) -> Response[Error | FrontendCustomDomainConflictError | VerifiedDomain]:
    """ Verify a domain

     Verifies the account's ownership of a domain and every name below it.
    Verify a registrable domain such as `example.com` to cover all of its
    subdomains, or a delegated subdomain you control.

    Publish a TXT record named `_volcano.<domain>`, then send this request.
    Without the record, the response is `409` with
    `code: ownership_verification_required` and the `required_record` to
    publish. Its value is the same on every request. The record must be
    served at that name itself; a record reached through a CNAME does not
    count.

    When another account verified the domain, publishing your record moves
    the domain to your account once that account's record is no longer
    published. Keep your record published so the domain stays yours.

    Verifying a domain the account already verified returns `200`.

    Args:
        body (VerifyDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCustomDomainConflictError | VerifiedDomain]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: VerifyDomainRequest,

) -> Error | FrontendCustomDomainConflictError | VerifiedDomain | None:
    """ Verify a domain

     Verifies the account's ownership of a domain and every name below it.
    Verify a registrable domain such as `example.com` to cover all of its
    subdomains, or a delegated subdomain you control.

    Publish a TXT record named `_volcano.<domain>`, then send this request.
    Without the record, the response is `409` with
    `code: ownership_verification_required` and the `required_record` to
    publish. Its value is the same on every request. The record must be
    served at that name itself; a record reached through a CNAME does not
    count.

    When another account verified the domain, publishing your record moves
    the domain to your account once that account's record is no longer
    published. Keep your record published so the domain stays yours.

    Verifying a domain the account already verified returns `200`.

    Args:
        body (VerifyDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCustomDomainConflictError | VerifiedDomain
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed

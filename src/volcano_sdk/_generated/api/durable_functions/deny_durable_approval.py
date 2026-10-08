from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_approval import DurableApproval
from ...models.durable_approval_decision_request import DurableApprovalDecisionRequest
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    approval_id: UUID | str,
    *,
    body: DurableApprovalDecisionRequest | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/durable-approvals/{approval_id}/deny".format(id=quote(str(id), safe=""),approval_id=quote(str(approval_id), safe=""),),
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableApproval | Error | None:
    if response.status_code == 200:
        response_200 = DurableApproval.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableApproval | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    approval_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DurableApprovalDecisionRequest | Unset = UNSET,

) -> Response[DurableApproval | Error]:
    """ Deny a durable approval

     Denies a pending approval. The workflow resumes with the decision; a
    denial is a value the workflow branches on, not an error.

    Only a person can decide: use the dashboard or a platform token from
    `volcano login`. Project access tokens are refused with `403`.

    Denying an approval that is already denied returns it unchanged.
    If the workflow cannot be reached right away, the decision still
    stands and Volcano keeps delivering it.

    Args:
        id (UUID):
        approval_id (UUID):
        body (DurableApprovalDecisionRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableApproval | Error]
     """


    kwargs = request_kwargs(
        id=id,
approval_id=approval_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    approval_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DurableApprovalDecisionRequest | Unset = UNSET,

) -> DurableApproval | Error | None:
    """ Deny a durable approval

     Denies a pending approval. The workflow resumes with the decision; a
    denial is a value the workflow branches on, not an error.

    Only a person can decide: use the dashboard or a platform token from
    `volcano login`. Project access tokens are refused with `403`.

    Denying an approval that is already denied returns it unchanged.
    If the workflow cannot be reached right away, the decision still
    stands and Volcano keeps delivering it.

    Args:
        id (UUID):
        approval_id (UUID):
        body (DurableApprovalDecisionRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableApproval | Error
     """


    return sync_detailed(
        id=id,
approval_id=approval_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    approval_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DurableApprovalDecisionRequest | Unset = UNSET,

) -> Response[DurableApproval | Error]:
    """ Deny a durable approval

     Denies a pending approval. The workflow resumes with the decision; a
    denial is a value the workflow branches on, not an error.

    Only a person can decide: use the dashboard or a platform token from
    `volcano login`. Project access tokens are refused with `403`.

    Denying an approval that is already denied returns it unchanged.
    If the workflow cannot be reached right away, the decision still
    stands and Volcano keeps delivering it.

    Args:
        id (UUID):
        approval_id (UUID):
        body (DurableApprovalDecisionRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableApproval | Error]
     """


    kwargs = request_kwargs(
        id=id,
approval_id=approval_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    approval_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DurableApprovalDecisionRequest | Unset = UNSET,

) -> DurableApproval | Error | None:
    """ Deny a durable approval

     Denies a pending approval. The workflow resumes with the decision; a
    denial is a value the workflow branches on, not an error.

    Only a person can decide: use the dashboard or a platform token from
    `volcano login`. Project access tokens are refused with `403`.

    Denying an approval that is already denied returns it unchanged.
    If the workflow cannot be reached right away, the decision still
    stands and Volcano keeps delivering it.

    Args:
        id (UUID):
        approval_id (UUID):
        body (DurableApprovalDecisionRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableApproval | Error
     """


    return (await asyncio_detailed(
        id=id,
approval_id=approval_id,
client=client,
body=body,

    )).parsed

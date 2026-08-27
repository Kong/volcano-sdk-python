from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_deployment_summary import ProjectDeploymentSummary
from ...models.summarize_project_deployments_resource_type import check_summarize_project_deployments_resource_type
from ...models.summarize_project_deployments_resource_type import SummarizeProjectDeploymentsResourceType
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    id: UUID,
    *,
    search: str | Unset = UNSET,
    resource_type: SummarizeProjectDeploymentsResourceType,
    created_after: datetime.datetime | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["search"] = search

    json_resource_type: str = resource_type
    params["resource_type"] = json_resource_type

    json_created_after: str | Unset = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["created_after"] = json_created_after


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/deployments/summary".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectDeploymentSummary | None:
    if response.status_code == 200:
        response_200 = ProjectDeploymentSummary.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectDeploymentSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    search: str | Unset = UNSET,
    resource_type: SummarizeProjectDeploymentsResourceType,
    created_after: datetime.datetime | Unset = UNSET,

) -> Response[Error | ProjectDeploymentSummary]:
    """ Summarize deployments in a project

     Summarizes deployment attempts for one comparable resource pipeline.
    Success rate uses conclusive outcomes only: active and deleted attempts
    are successful; failed and degraded attempts are failures; in-progress
    and superseded attempts are excluded. Median build duration includes
    completed, non-superseded attempts with recorded build work,
    including failed builds.

    Args:
        id (UUID):
        search (str | Unset):
        resource_type (SummarizeProjectDeploymentsResourceType):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectDeploymentSummary]
     """


    kwargs = _get_kwargs(
        id=id,
search=search,
resource_type=resource_type,
created_after=created_after,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    search: str | Unset = UNSET,
    resource_type: SummarizeProjectDeploymentsResourceType,
    created_after: datetime.datetime | Unset = UNSET,

) -> Error | ProjectDeploymentSummary | None:
    """ Summarize deployments in a project

     Summarizes deployment attempts for one comparable resource pipeline.
    Success rate uses conclusive outcomes only: active and deleted attempts
    are successful; failed and degraded attempts are failures; in-progress
    and superseded attempts are excluded. Median build duration includes
    completed, non-superseded attempts with recorded build work,
    including failed builds.

    Args:
        id (UUID):
        search (str | Unset):
        resource_type (SummarizeProjectDeploymentsResourceType):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectDeploymentSummary
     """


    return sync_detailed(
        id=id,
client=client,
search=search,
resource_type=resource_type,
created_after=created_after,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    search: str | Unset = UNSET,
    resource_type: SummarizeProjectDeploymentsResourceType,
    created_after: datetime.datetime | Unset = UNSET,

) -> Response[Error | ProjectDeploymentSummary]:
    """ Summarize deployments in a project

     Summarizes deployment attempts for one comparable resource pipeline.
    Success rate uses conclusive outcomes only: active and deleted attempts
    are successful; failed and degraded attempts are failures; in-progress
    and superseded attempts are excluded. Median build duration includes
    completed, non-superseded attempts with recorded build work,
    including failed builds.

    Args:
        id (UUID):
        search (str | Unset):
        resource_type (SummarizeProjectDeploymentsResourceType):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectDeploymentSummary]
     """


    kwargs = _get_kwargs(
        id=id,
search=search,
resource_type=resource_type,
created_after=created_after,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    search: str | Unset = UNSET,
    resource_type: SummarizeProjectDeploymentsResourceType,
    created_after: datetime.datetime | Unset = UNSET,

) -> Error | ProjectDeploymentSummary | None:
    """ Summarize deployments in a project

     Summarizes deployment attempts for one comparable resource pipeline.
    Success rate uses conclusive outcomes only: active and deleted attempts
    are successful; failed and degraded attempts are failures; in-progress
    and superseded attempts are excluded. Median build duration includes
    completed, non-superseded attempts with recorded build work,
    including failed builds.

    Args:
        id (UUID):
        search (str | Unset):
        resource_type (SummarizeProjectDeploymentsResourceType):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectDeploymentSummary
     """


    return (await asyncio_detailed(
        id=id,
client=client,
search=search,
resource_type=resource_type,
created_after=created_after,

    )).parsed

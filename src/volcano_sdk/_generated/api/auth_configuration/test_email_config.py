from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.test_email_request import TestEmailRequest
from ...models.test_email_response import TestEmailResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: TestEmailRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/auth/config/test-email".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | TestEmailResponse | None:
    if response.status_code == 200:
        response_200 = TestEmailResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 502:
        response_502 = cast(Any, None)
        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | TestEmailResponse]:
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
    body: TestEmailRequest,

) -> Response[Any | TestEmailResponse]:
    r""" Send a test email using the project's saved SMTP config

     Sends a diagnostic email to `to_email` using the project's
    persisted `auth_config` SMTP credentials. If `html_body` or
    `text_body` is supplied, the override path is taken: those
    values (plus optional `subject`) are rendered through
    html/text templates against the project's `Data` and
    used as the body — used by the template editor's \"Send Test\"
    affordance to preview an unsaved template. With both bodies
    omitted, a hardcoded diagnostic message is sent and any
    `subject` field is ignored. Sending `subject` alone (no
    bodies) is rejected with 400 to avoid a silently-dropped
    subject or a blank message. Also rejects with 400 if
    `email_enabled=false` or `smtp_host` is empty.

    Args:
        id (UUID):
        body (TestEmailRequest): When `html_body` or `text_body` is provided the backend renders
            those (plus optional `subject`) through html/text templates
            against the standard `Data` (ProjectName, Name, SiteURL)
            and sends the result — used by the template-editor "Send Test"
            affordance to preview an unsaved template. When both bodies are
            omitted a hardcoded diagnostic message is sent to verify SMTP
            credentials and `subject` is ignored. Sending `subject` alone
            (without a body) is rejected with 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | TestEmailResponse]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: TestEmailRequest,

) -> Any | TestEmailResponse | None:
    r""" Send a test email using the project's saved SMTP config

     Sends a diagnostic email to `to_email` using the project's
    persisted `auth_config` SMTP credentials. If `html_body` or
    `text_body` is supplied, the override path is taken: those
    values (plus optional `subject`) are rendered through
    html/text templates against the project's `Data` and
    used as the body — used by the template editor's \"Send Test\"
    affordance to preview an unsaved template. With both bodies
    omitted, a hardcoded diagnostic message is sent and any
    `subject` field is ignored. Sending `subject` alone (no
    bodies) is rejected with 400 to avoid a silently-dropped
    subject or a blank message. Also rejects with 400 if
    `email_enabled=false` or `smtp_host` is empty.

    Args:
        id (UUID):
        body (TestEmailRequest): When `html_body` or `text_body` is provided the backend renders
            those (plus optional `subject`) through html/text templates
            against the standard `Data` (ProjectName, Name, SiteURL)
            and sends the result — used by the template-editor "Send Test"
            affordance to preview an unsaved template. When both bodies are
            omitted a hardcoded diagnostic message is sent to verify SMTP
            credentials and `subject` is ignored. Sending `subject` alone
            (without a body) is rejected with 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | TestEmailResponse
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: TestEmailRequest,

) -> Response[Any | TestEmailResponse]:
    r""" Send a test email using the project's saved SMTP config

     Sends a diagnostic email to `to_email` using the project's
    persisted `auth_config` SMTP credentials. If `html_body` or
    `text_body` is supplied, the override path is taken: those
    values (plus optional `subject`) are rendered through
    html/text templates against the project's `Data` and
    used as the body — used by the template editor's \"Send Test\"
    affordance to preview an unsaved template. With both bodies
    omitted, a hardcoded diagnostic message is sent and any
    `subject` field is ignored. Sending `subject` alone (no
    bodies) is rejected with 400 to avoid a silently-dropped
    subject or a blank message. Also rejects with 400 if
    `email_enabled=false` or `smtp_host` is empty.

    Args:
        id (UUID):
        body (TestEmailRequest): When `html_body` or `text_body` is provided the backend renders
            those (plus optional `subject`) through html/text templates
            against the standard `Data` (ProjectName, Name, SiteURL)
            and sends the result — used by the template-editor "Send Test"
            affordance to preview an unsaved template. When both bodies are
            omitted a hardcoded diagnostic message is sent to verify SMTP
            credentials and `subject` is ignored. Sending `subject` alone
            (without a body) is rejected with 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | TestEmailResponse]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: TestEmailRequest,

) -> Any | TestEmailResponse | None:
    r""" Send a test email using the project's saved SMTP config

     Sends a diagnostic email to `to_email` using the project's
    persisted `auth_config` SMTP credentials. If `html_body` or
    `text_body` is supplied, the override path is taken: those
    values (plus optional `subject`) are rendered through
    html/text templates against the project's `Data` and
    used as the body — used by the template editor's \"Send Test\"
    affordance to preview an unsaved template. With both bodies
    omitted, a hardcoded diagnostic message is sent and any
    `subject` field is ignored. Sending `subject` alone (no
    bodies) is rejected with 400 to avoid a silently-dropped
    subject or a blank message. Also rejects with 400 if
    `email_enabled=false` or `smtp_host` is empty.

    Args:
        id (UUID):
        body (TestEmailRequest): When `html_body` or `text_body` is provided the backend renders
            those (plus optional `subject`) through html/text templates
            against the standard `Data` (ProjectName, Name, SiteURL)
            and sends the result — used by the template-editor "Send Test"
            affordance to preview an unsaved template. When both bodies are
            omitted a hardcoded diagnostic message is sent to verify SMTP
            credentials and `subject` is ignored. Sending `subject` alone
            (without a body) is rejected with 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | TestEmailResponse
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed

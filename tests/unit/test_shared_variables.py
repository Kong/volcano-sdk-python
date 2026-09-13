import json
from uuid import UUID

import httpx

from volcano_sdk._generated.api.projects import replace_shared_variables
from volcano_sdk._generated.client import AuthenticatedClient
from volcano_sdk._generated.models import ReplaceSharedVariablesBody

DIGEST = "23519a43c66b4c342f25b32e09797ec5f3fc0be388cd8243fb3449afbdce4013"


def test_replace_shared_variables_sends_digest_precondition() -> None:
    project_id = UUID("00000000-0000-4000-8000-000000000002")
    body = ReplaceSharedVariablesBody(
        shared_variables=["API_KEY", "REGION"],
        expected_shared_variables_digest=DIGEST,
    )

    def respond(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        assert request.url.path == f"/projects/{project_id}/shared-variables"
        assert json.loads(request.content) == {
            "shared_variables": ["API_KEY", "REGION"],
            "expected_shared_variables_digest": DIGEST,
        }
        return httpx.Response(204)

    with httpx.Client(
        base_url="https://api.example.com", transport=httpx.MockTransport(respond)
    ) as http:
        client = AuthenticatedClient(
            base_url="https://api.example.com", token="test-token"
        ).set_httpx_client(http)
        response = replace_shared_variables.sync_detailed(
            project_id, client=client, body=body
        )

    assert response.status_code == 204

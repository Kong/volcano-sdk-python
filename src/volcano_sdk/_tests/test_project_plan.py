"""Keep project response plan names aligned with the public API."""

from __future__ import annotations

import pytest

from volcano_sdk._generated.models.project import Project


@pytest.mark.parametrize("plan", ["HOBBY", "SUPERAGENT"])
def test_project_response_accepts_public_plan_name(plan: str) -> None:
    project = Project.from_dict(
        {
            "id": "12345678-1234-1234-1234-123456789012",
            "name": "example",
            "status": "active",
            "plan": plan,
            "all_regions": True,
            "selected_regions": [],
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
    )
    assert project.plan == plan

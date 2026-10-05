from __future__ import annotations

import httpx


def upload_response(size: int = 7) -> httpx.Response:
    return httpx.Response(
        201,
        json={
            "id": "00000000-0000-4000-8000-000000000020",
            "bucket_id": "00000000-0000-4000-8000-000000000030",
            "name": "payload.bin",
            "is_public": False,
            "size": size,
            "mime_type": "application/octet-stream",
            "metadata": {},
            "owner_id": "00000000-0000-4000-8000-000000000010",
            "created_at": "2026-09-08T12:00:00Z",
            "updated_at": "2026-09-08T12:00:00Z",
        },
    )

from __future__ import annotations

import base64
import json


def access_token(version: str = "original") -> str:
    payload = (
        base64.urlsafe_b64encode(
            json.dumps(
                {
                    "session_id": "00000000-0000-4000-8000-000000000010",
                    "version": version,
                }
            ).encode()
        )
        .decode()
        .rstrip("=")
    )
    return f"header.{payload}.signature"

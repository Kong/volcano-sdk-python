"""Reproducible seeds and failure artifacts for SDK properties."""

from __future__ import annotations

import os
import secrets
from pathlib import Path

from hypothesis import settings

PROPERTY_SEED = int(os.environ.get("VOLCANO_PROPERTY_SEED", str(secrets.randbits(64))))


def configure_properties() -> None:
    """Record the run seed and keep Hypothesis's normal health checks enabled."""
    directory = Path("reports/hypothesis")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "seed.txt").write_text(f"{PROPERTY_SEED}\n", encoding="utf-8")
    settings.register_profile("sdk", max_examples=200, print_blob=True)
    settings.load_profile("sdk")


configure_properties()

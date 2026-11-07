from typing import Literal

LavaflowCommitOrigin = Literal['client_reported', 'client_reported_repository', 'push', 'repository']

LAVAFLOW_COMMIT_ORIGIN_VALUES: set[LavaflowCommitOrigin] = { 'client_reported', 'client_reported_repository', 'push', 'repository',  }

def check_lavaflow_commit_origin(value: str) -> LavaflowCommitOrigin:
    if value in LAVAFLOW_COMMIT_ORIGIN_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_COMMIT_ORIGIN_VALUES!r}")

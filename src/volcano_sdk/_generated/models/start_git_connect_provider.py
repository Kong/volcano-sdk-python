from typing import Literal

StartGitConnectProvider = Literal['github']

START_GIT_CONNECT_PROVIDER_VALUES: set[StartGitConnectProvider] = { 'github',  }

def check_start_git_connect_provider(value: str) -> StartGitConnectProvider:
    if value in START_GIT_CONNECT_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {START_GIT_CONNECT_PROVIDER_VALUES!r}")

from typing import Literal

AutofixPullRequestSkipped = Literal['low_confidence', 'no_patch', 'not_fixable', 'permission_missing', 'publish_failed', 'pull_request_open', 'repository_changed', 'source_unavailable']

AUTOFIX_PULL_REQUEST_SKIPPED_VALUES: set[AutofixPullRequestSkipped] = { 'low_confidence', 'no_patch', 'not_fixable', 'permission_missing', 'publish_failed', 'pull_request_open', 'repository_changed', 'source_unavailable',  }

def check_autofix_pull_request_skipped(value: str) -> AutofixPullRequestSkipped:
    if value in AUTOFIX_PULL_REQUEST_SKIPPED_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_PULL_REQUEST_SKIPPED_VALUES!r}")

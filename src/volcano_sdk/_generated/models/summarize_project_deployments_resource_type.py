from typing import Literal

SummarizeProjectDeploymentsResourceType = Literal['frontend', 'function']

SUMMARIZE_PROJECT_DEPLOYMENTS_RESOURCE_TYPE_VALUES: set[SummarizeProjectDeploymentsResourceType] = { 'frontend', 'function',  }

def check_summarize_project_deployments_resource_type(value: str) -> SummarizeProjectDeploymentsResourceType:
    if value in SUMMARIZE_PROJECT_DEPLOYMENTS_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SUMMARIZE_PROJECT_DEPLOYMENTS_RESOURCE_TYPE_VALUES!r}")

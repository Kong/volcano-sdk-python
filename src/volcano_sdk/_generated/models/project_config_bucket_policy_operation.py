from typing import Literal

ProjectConfigBucketPolicyOperation = Literal['DELETE', 'INSERT', 'SELECT', 'UPDATE']

PROJECT_CONFIG_BUCKET_POLICY_OPERATION_VALUES: set[ProjectConfigBucketPolicyOperation] = { 'DELETE', 'INSERT', 'SELECT', 'UPDATE',  }

def check_project_config_bucket_policy_operation(value: str) -> ProjectConfigBucketPolicyOperation:
    if value in PROJECT_CONFIG_BUCKET_POLICY_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_BUCKET_POLICY_OPERATION_VALUES!r}")

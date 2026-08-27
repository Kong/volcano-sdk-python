from typing import Literal

CreateDatabaseRequestRegion = Literal['aws-ap-southeast-1', 'aws-ap-southeast-2', 'aws-eu-central-1', 'aws-eu-west-2', 'aws-sa-east-1', 'aws-us-east-1', 'aws-us-east-2', 'aws-us-west-2']

CREATE_DATABASE_REQUEST_REGION_VALUES: set[CreateDatabaseRequestRegion] = { 'aws-ap-southeast-1', 'aws-ap-southeast-2', 'aws-eu-central-1', 'aws-eu-west-2', 'aws-sa-east-1', 'aws-us-east-1', 'aws-us-east-2', 'aws-us-west-2',  }

def check_create_database_request_region(value: str) -> CreateDatabaseRequestRegion:
    if value in CREATE_DATABASE_REQUEST_REGION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_DATABASE_REQUEST_REGION_VALUES!r}")

from typing import Literal

CreateProjectRequestTemplateId = Literal['collab-pad', 'official-starter', 'pixel-board', 'trellini']

CREATE_PROJECT_REQUEST_TEMPLATE_ID_VALUES: set[CreateProjectRequestTemplateId] = { 'collab-pad', 'official-starter', 'pixel-board', 'trellini',  }

def check_create_project_request_template_id(value: str) -> CreateProjectRequestTemplateId:
    if value in CREATE_PROJECT_REQUEST_TEMPLATE_ID_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_PROJECT_REQUEST_TEMPLATE_ID_VALUES!r}")

from typing import Literal

ProjectPlan = Literal['HOBBY', 'SUPERAGENT']

PROJECT_PLAN_VALUES: set[ProjectPlan] = { 'HOBBY', 'SUPERAGENT',  }

def check_project_plan(value: str) -> ProjectPlan:
    if value in PROJECT_PLAN_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_PLAN_VALUES!r}")

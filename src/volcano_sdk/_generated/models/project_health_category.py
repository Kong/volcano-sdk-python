from typing import Literal

ProjectHealthCategory = Literal['lifecycle', 'storage']

PROJECT_HEALTH_CATEGORY_VALUES: set[ProjectHealthCategory] = { 'lifecycle', 'storage',  }

def check_project_health_category(value: str) -> ProjectHealthCategory:
    if value in PROJECT_HEALTH_CATEGORY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_HEALTH_CATEGORY_VALUES!r}")

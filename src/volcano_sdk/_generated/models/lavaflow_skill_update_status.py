from typing import Literal

LavaflowSkillUpdateStatus = Literal['active', 'retired']

LAVAFLOW_SKILL_UPDATE_STATUS_VALUES: set[LavaflowSkillUpdateStatus] = { 'active', 'retired',  }

def check_lavaflow_skill_update_status(value: str) -> LavaflowSkillUpdateStatus:
    if value in LAVAFLOW_SKILL_UPDATE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_UPDATE_STATUS_VALUES!r}")

from typing import Literal

LavaflowSkillStatus = Literal['active', 'proposed', 'retired']

LAVAFLOW_SKILL_STATUS_VALUES: set[LavaflowSkillStatus] = { 'active', 'proposed', 'retired',  }

def check_lavaflow_skill_status(value: str) -> LavaflowSkillStatus:
    if value in LAVAFLOW_SKILL_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_STATUS_VALUES!r}")

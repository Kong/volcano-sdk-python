from typing import Literal

LavaflowSkillScope = Literal['project', 'volcano']

LAVAFLOW_SKILL_SCOPE_VALUES: set[LavaflowSkillScope] = { 'project', 'volcano',  }

def check_lavaflow_skill_scope(value: str) -> LavaflowSkillScope:
    if value in LAVAFLOW_SKILL_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_SCOPE_VALUES!r}")

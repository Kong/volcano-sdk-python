from typing import Literal

LavaflowSkillSourceAct = Literal['comment', 'commit', 'review']

LAVAFLOW_SKILL_SOURCE_ACT_VALUES: set[LavaflowSkillSourceAct] = { 'comment', 'commit', 'review',  }

def check_lavaflow_skill_source_act(value: str) -> LavaflowSkillSourceAct:
    if value in LAVAFLOW_SKILL_SOURCE_ACT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_SOURCE_ACT_VALUES!r}")

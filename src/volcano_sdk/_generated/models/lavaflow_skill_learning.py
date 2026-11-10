from typing import Literal

LavaflowSkillLearning = Literal['auto', 'off', 'review']

LAVAFLOW_SKILL_LEARNING_VALUES: set[LavaflowSkillLearning] = { 'auto', 'off', 'review',  }

def check_lavaflow_skill_learning(value: str) -> LavaflowSkillLearning:
    if value in LAVAFLOW_SKILL_LEARNING_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_LEARNING_VALUES!r}")

from typing import Literal

LavaflowSkillSourceKind = Literal['person', 'run']

LAVAFLOW_SKILL_SOURCE_KIND_VALUES: set[LavaflowSkillSourceKind] = { 'person', 'run',  }

def check_lavaflow_skill_source_kind(value: str) -> LavaflowSkillSourceKind:
    if value in LAVAFLOW_SKILL_SOURCE_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_SOURCE_KIND_VALUES!r}")

from typing import Literal

LavaflowSkillRetiredReason = Literal['gate', 'harmful', 'owner', 'repository_changed', 'stale', 'unused']

LAVAFLOW_SKILL_RETIRED_REASON_VALUES: set[LavaflowSkillRetiredReason] = { 'gate', 'harmful', 'owner', 'repository_changed', 'stale', 'unused',  }

def check_lavaflow_skill_retired_reason(value: str) -> LavaflowSkillRetiredReason:
    if value in LAVAFLOW_SKILL_RETIRED_REASON_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_RETIRED_REASON_VALUES!r}")

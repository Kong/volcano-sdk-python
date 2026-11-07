from typing import Literal

LavaflowSkillErrorRulesItem = Literal['characters', 'credential', 'credential_scan', 'directive', 'email', 'link', 'policy', 'read_value', 'sanitizer', 'secret', 'shape']

LAVAFLOW_SKILL_ERROR_RULES_ITEM_VALUES: set[LavaflowSkillErrorRulesItem] = { 'characters', 'credential', 'credential_scan', 'directive', 'email', 'link', 'policy', 'read_value', 'sanitizer', 'secret', 'shape',  }

def check_lavaflow_skill_error_rules_item(value: str) -> LavaflowSkillErrorRulesItem:
    if value in LAVAFLOW_SKILL_ERROR_RULES_ITEM_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKILL_ERROR_RULES_ITEM_VALUES!r}")

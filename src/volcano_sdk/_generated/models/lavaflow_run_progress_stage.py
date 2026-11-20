from typing import Literal

LavaflowRunProgressStage = Literal['diagnosing', 'fixing', 'merge_queued', 'queued', 'reviewing', 'waiting_for_checks']

LAVAFLOW_RUN_PROGRESS_STAGE_VALUES: set[LavaflowRunProgressStage] = { 'diagnosing', 'fixing', 'merge_queued', 'queued', 'reviewing', 'waiting_for_checks',  }

def check_lavaflow_run_progress_stage(value: str) -> LavaflowRunProgressStage:
    if value in LAVAFLOW_RUN_PROGRESS_STAGE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_RUN_PROGRESS_STAGE_VALUES!r}")

from collections.abc import Callable
from typing import ParamSpec, Protocol

from behave.runner import Context

_P = ParamSpec("_P")

class _StepFunction(Protocol[_P]):
    def __call__(
        self, context: Context, *args: _P.args, **kwargs: _P.kwargs
    ) -> None: ...

def given(
    step_text: str, **kwargs: object
) -> Callable[[_StepFunction[_P]], _StepFunction[_P]]: ...
def when(
    step_text: str, **kwargs: object
) -> Callable[[_StepFunction[_P]], _StepFunction[_P]]: ...
def then(
    step_text: str, **kwargs: object
) -> Callable[[_StepFunction[_P]], _StepFunction[_P]]: ...

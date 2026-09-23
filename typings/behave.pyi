from collections.abc import Callable
from typing import Concatenate, ParamSpec

from behave.runner import Context

_P = ParamSpec("_P")

def given(
    step_text: str, **kwargs: object
) -> Callable[
    [Callable[Concatenate[Context, _P], None]],
    Callable[Concatenate[Context, _P], None],
]: ...
def when(
    step_text: str, **kwargs: object
) -> Callable[
    [Callable[Concatenate[Context, _P], None]],
    Callable[Concatenate[Context, _P], None],
]: ...
def then(
    step_text: str, **kwargs: object
) -> Callable[
    [Callable[Concatenate[Context, _P], None]],
    Callable[Concatenate[Context, _P], None],
]: ...

from collections.abc import Callable
from typing import Concatenate, TypeVar

from behave.runner import Context

_F = TypeVar("_F", bound=Callable[Concatenate[Context, ...], None])

def given(step_text: str, **kwargs: object) -> Callable[[_F], _F]: ...
def when(step_text: str, **kwargs: object) -> Callable[[_F], _F]: ...
def then(step_text: str, **kwargs: object) -> Callable[[_F], _F]: ...

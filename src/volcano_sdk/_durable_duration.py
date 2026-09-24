"""Validate duration strings, mappings, and whole-second values."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeGuard

if TYPE_CHECKING:
    from collections.abc import Callable

_DURATION_FIELDS = ("days", "hours", "minutes", "seconds")
_DURATION_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
_FIELD_UNITS = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}


def to_seconds(value: object, field_name: str) -> int:
    """Read a duration as whole seconds.

    Accepts `"30s"`, `"1m30s"`, a whole number of seconds, or a mapping of
    days/hours/minutes/seconds.

    Returns:
        The duration in non-negative whole seconds.

    Raises:
        TypeError: The value is not a supported numeric, mapping, or string form.

    """
    if isinstance(value, (int, float)):
        return _numeric_seconds(value, field_name)
    if _is_string_keyed_mapping(value):
        return _mapping_seconds(value, field_name)
    if isinstance(value, dict):
        raise TypeError(_duration_type_error(field_name))
    if not isinstance(value, str):
        raise TypeError(_duration_type_error(field_name))
    return _parse_duration(value.strip(), field_name)


def _is_string_keyed_mapping(value: object) -> TypeGuard[dict[str, object]]:
    if not _is_object_dict(value):
        return False
    return all(isinstance(key, str) for key in value)


def _is_object_dict(value: object) -> TypeGuard[dict[object, object]]:
    return isinstance(value, dict)


def _numeric_seconds(value: object, field_name: str) -> int:
    if isinstance(value, bool):
        raise TypeError(_duration_type_error(field_name))
    if not isinstance(value, int):
        # Fractions would silently change the requested wait.
        message = f"{field_name} must be a whole number of seconds, not a fraction"
        raise TypeError(message)
    if value < 0:
        message = f"{field_name} must be a non-negative whole number of seconds"
        raise ValueError(message)
    return value


def _duration_type_error(field_name: str) -> str:
    return (
        f"{field_name} must be a duration string, a whole number of seconds, "
        f"or a mapping of {', '.join(_DURATION_FIELDS)}"
    )


def _mapping_seconds(value: dict[str, object], field_name: str) -> int:
    """Read the mapping form, refusing keys it does not have.

    Unknown keys are the reason this checks rather than forwards: a
    `{"milliseconds": 500}` would otherwise be a duration of nothing.

    Returns:
        The sum of the supplied duration fields, converted to seconds.

    Raises:
        TypeError: The mapping has unknown keys or no non-null duration fields.

    """
    unknown = sorted(key for key in value if key not in _DURATION_FIELDS)
    if unknown:
        message = (
            f"{field_name} duration takes {', '.join(_DURATION_FIELDS)} "
            f"(got {', '.join(unknown)})"
        )
        raise TypeError(message)
    if not any(value.get(key) is not None for key in _DURATION_FIELDS):
        message = f"{field_name} duration needs one of {', '.join(_DURATION_FIELDS)}"
        raise TypeError(message)
    return sum(
        _duration_part(value.get(key), field_name, key) * _FIELD_UNITS[key]
        for key in _DURATION_FIELDS
    )


def _duration_part(part: object, field_name: str, key: str) -> int:
    if part is None:
        return 0
    if isinstance(part, bool) or not isinstance(part, int) or part < 0:
        message = f"{field_name} duration {key} must be a non-negative whole number"
        raise ValueError(message)
    return part


def _parse_duration(text: str, field_name: str) -> int:
    """Scan a whole number and a unit, repeated.

    Scanned rather than matched because every pattern for this grammar is
    either unreadable or the kind with adjacent quantifiers that backtracks on
    a hostile string. Whole numbers only -- "90m" says what "1.5h" would.

    Returns:
        The sum of the parsed duration segments in seconds.

    Raises:
        ValueError: The text is empty or contains an invalid number or unit.

    """
    parts: list[int] = []
    at = 0
    # Each valid iteration consumes input, so its length bounds the scan.
    for _ in text:
        at = _scan(text, at, lambda char: char == " ")
        if at == len(text):
            break
        number_end = _scan(text, at, str.isdigit)
        unit_end = _scan(text, number_end, str.islower)
        unit = text[number_end:unit_end]
        if number_end == at or unit not in _DURATION_UNITS:
            break
        parts.append(int(text[at:number_end]) * _DURATION_UNITS[unit])
        at = unit_end
    if not parts or at != len(text):
        message = (
            f"{field_name} must be a duration in whole seconds, such as '30s', "
            f"'5m', '2h', '1d' or '1m30s' (got {text!r})"
        )
        raise ValueError(message)
    return sum(parts)


def _scan(text: str, start: int, accept: Callable[[str], bool]) -> int:
    for at in range(start, len(text)):
        if not accept(text[at]):
            return at
    return len(text)

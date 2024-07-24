import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import TypeVar

from fastapi.routing import APIRoute


def utc_now() -> datetime:
    return datetime.now(UTC)


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def human_readable_size(num: float, suffix: str = "B") -> str:
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Y{suffix}"


def generate_unique_openapi_id(route: APIRoute) -> str:
    return f"{route.tags[0]}:{route.name}"


E = TypeVar("E", bound=Enum)


def enum_to_set(enum_class: type[E], values: str) -> set[E]:
    """
    Converts a space-separated string of enum values into a set of the enum members.
    """
    return {
        enum_class(value.strip())
        for value in values.split()
        if value.strip() in enum_class._value2member_map_
    }


def enum_to_list(enum_class: type[E], values: str) -> list[E]:
    """
    Converts a space-separated string of enum values into a list of the enum members.
    """
    return list(enum_to_set(enum_class, values))


def enum_list_all(enum_class: type[E]) -> list[str]:
    """
    Lists all values of the given enum class.
    """
    return [member.value for member in enum_class]


def ensure_str(value: str | bytes) -> str:
    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return value.decode("utf-8")
    else:
        raise ValueError("Input value must be str or bytes.")


def ensure_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    elif isinstance(value, str):
        return value.encode("utf-8")
    else:
        raise ValueError("Input value must be str or bytes.")

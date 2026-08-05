from typing import Any

from pydantic import BaseModel


class TableFilter(BaseModel):
    """Single TanStack Table column filter (`filters[]` query parameter):
    `{id, value}`, where `id` is the column key and `value` the filter
    value (any JSON type)."""

    id: str
    value: Any


class TableSort(BaseModel):
    """Single TanStack Table sort entry (`sorting[]` query parameter):
    `{id, desc}`, where `id` is the column key and `desc` the sort
    direction."""

    id: str
    desc: bool

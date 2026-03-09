from __future__ import annotations

from dataclasses import dataclass
from typing import Any

JSONLike = dict[str, Any] | list[Any] | str | None


@dataclass(slots=True, frozen=True)
class SMSResponse:
    ok: bool
    status_code: int
    data: JSONLike
    raw_text: str
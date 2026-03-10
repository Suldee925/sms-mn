from __future__ import annotations

import json
from abc import ABC, abstractmethod

import httpx

from sms_mn.models import JSONLike, SMSResponse


class BaseSMSProvider(ABC):
    name: str = "base"

    @abstractmethod
    def build_request(
        self,
        *,
        to: str,
        message: str,
    ) -> tuple[str, str, dict[str, str], dict[str, object] | None]:
        """
        Returns:
            method, url, headers, json_body
        """

    def parse_response(self, response: httpx.Response) -> SMSResponse:
        raw_text = response.text

        try:
            data: JSONLike = response.json()
        except json.JSONDecodeError:
            data = raw_text

        return SMSResponse(
            ok=response.is_success,
            status_code=response.status_code,
            data=data,
            raw_text=raw_text,
            provider=self.name,
        )
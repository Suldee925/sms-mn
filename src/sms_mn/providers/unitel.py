from __future__ import annotations

from sms_mn._validators import validate_message, validate_phone_number
from sms_mn.exceptions import SMSValidationError

from .base import BaseSMSProvider

DEFAULT_UNITEL_BASE_URL = "https://pn.unitel.mn/api/message/send/sms"


class UnitelProvider(BaseSMSProvider):
    name = "unitel"

    def __init__(self, api_key: str, *, base_url: str = DEFAULT_UNITEL_BASE_URL) -> None:
        api_key = api_key.strip()
        base_url = base_url.strip()

        if not api_key:
            raise SMSValidationError("`api_key` must not be empty.")
        if not base_url:
            raise SMSValidationError("`base_url` must not be empty.")

        self.api_key = api_key
        self.base_url = base_url

    def build_request(
        self,
        *,
        to: str,
        message: str,
    ) -> tuple[str, str, dict[str, str], dict[str, object] | None]:
        payload = {
            "to": validate_phone_number(to),
            "message": validate_message(message),
        }
        url = f"{self.base_url}?enc={self.api_key}"

        headers = {
            "Content-Type": "application/json",
        }

        return "POST", url, headers, payload
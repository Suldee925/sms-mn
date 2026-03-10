from __future__ import annotations

from urllib.parse import urlencode

from sms_mn._validators import validate_message, validate_phone_number
from sms_mn.exceptions import SMSValidationError

from .base import BaseSMSProvider


class MobicomProvider(BaseSMSProvider):
    name = "mobicom"

    def __init__(
        self,
        *,
        base_url: str,
        servicename: str,
        username: str,
        sender: str,
    ) -> None:
        base_url = base_url.strip()
        servicename = servicename.strip()
        username = username.strip()
        sender = sender.strip()

        if not base_url:
            raise SMSValidationError("`base_url` must not be empty.")
        if not servicename:
            raise SMSValidationError("`servicename` must not be empty.")
        if not username:
            raise SMSValidationError("`username` must not be empty.")
        if not sender:
            raise SMSValidationError("`sender` must not be empty.")

        self.base_url = base_url
        self.servicename = servicename
        self.username = username
        self.sender = sender

    def build_request(
        self,
        *,
        to: str,
        message: str,
    ) -> tuple[str, str, dict[str, str], dict[str, object] | None]:
        params = {
            "servicename": self.servicename,
            "username": self.username,
            "from": self.sender,
            "to": validate_phone_number(to),
            "msg": validate_message(message),
        }

        url = f"{self.base_url}?{urlencode(params)}"
        headers: dict[str, str] = {}

        return "GET", url, headers, None
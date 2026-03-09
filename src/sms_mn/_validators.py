from __future__ import annotations

from .exceptions import SMSValidationError

MAX_MESSAGE_LENGTH = 1600


def validate_phone_number(to: str) -> str:
    normalized = to.strip()
    digits = normalized.replace("+", "")

    if not digits.isdigit():
        raise SMSValidationError("`to` must contain only digits, optionally prefixed with '+'.")

    if len(digits) < 8 or len(digits) > 15:
        raise SMSValidationError("`to` must be between 8 and 15 digits.")

    return normalized


def validate_message(message: str) -> str:
    normalized = message.strip()

    if not normalized:
        raise SMSValidationError("`message` must not be empty.")

    if len(normalized) > MAX_MESSAGE_LENGTH:
        raise SMSValidationError(
            f"`message` must be at most {MAX_MESSAGE_LENGTH} characters long."
        )

    return normalized
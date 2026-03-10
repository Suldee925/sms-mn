import pytest

from sms_mn import SMSValidationError
from sms_mn.utils import validate_message, validate_phone_number


def test_validate_phone_number_success() -> None:
    assert validate_phone_number("88111111") == "88111111"


def test_validate_phone_number_invalid() -> None:
    with pytest.raises(SMSValidationError):
        validate_phone_number("88-111-111")


def test_validate_message_success() -> None:
    assert validate_message(" hello ") == "hello"


def test_validate_message_empty() -> None:
    with pytest.raises(SMSValidationError):
        validate_message("   ")
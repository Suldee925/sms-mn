class SMSMNError(Exception):
    """Base exception for sms-mn."""


class SMSValidationError(SMSMNError):
    """Raised when input data is invalid."""


class SMSAPIError(SMSMNError):
    """Raised when the SMS API returns a non-success response."""

    def __init__(self, message: str, *, status_code: int, response_text: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class SMSNetworkError(SMSMNError):
    """Raised when the SMS API cannot be reached."""
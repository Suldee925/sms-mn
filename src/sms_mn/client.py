from __future__ import annotations

import asyncio
import json
import time

import httpx

from ._validators import validate_message, validate_phone_number
from .exceptions import SMSAPIError, SMSNetworkError, SMSValidationError
from .models import JSONLike, SMSResponse

DEFAULT_BASE_URL = "https://pn.unitel.mn/api/message/send/sms"
DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_RETRY_DELAY = 0.5
USER_AGENT = "sms-mn/0.1.0"


class _BaseSMSClient:
    def __init__(
        self,
        api_key: str,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        base_url: str = DEFAULT_BASE_URL,
    ) -> None:
        api_key = api_key.strip()
        base_url = base_url.strip()

        if not api_key:
            raise SMSValidationError("`api_key` must not be empty.")
        if timeout <= 0:
            raise SMSValidationError("`timeout` must be greater than 0.")
        if max_retries < 0:
            raise SMSValidationError("`max_retries` must be 0 or greater.")
        if retry_delay < 0:
            raise SMSValidationError("`retry_delay` must be 0 or greater.")
        if not base_url:
            raise SMSValidationError("`base_url` must not be empty.")

        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.base_url = base_url

    def _build_url(self) -> str:
        return f"{self.base_url}?enc={self.api_key}"

    def _build_payload(self, to: str, message: str) -> dict[str, str]:
        validated_to = validate_phone_number(to)
        validated_message = validate_message(message)
        return {
            "to": validated_to,
            "message": validated_message,
        }

    @staticmethod
    def _parse_response(response: httpx.Response) -> SMSResponse:
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
        )


class SMSClient(_BaseSMSClient):
    def __init__(
        self,
        api_key: str,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        base_url: str = DEFAULT_BASE_URL,
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            api_key,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            base_url=base_url,
        )

        self._owns_client = client is None
        self._client = client or httpx.Client(
            timeout=self.timeout,
            headers={
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> SMSClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ) -> None:
        self.close()

    def send(self, to: str, message: str) -> SMSResponse:
        payload = self._build_payload(to, message)
        url = self._build_url()

        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self._client.post(url, json=payload)
                parsed = self._parse_response(response)

                if not response.is_success:
                    raise SMSAPIError(
                        "SMS API returned a non-success response.",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                return parsed

            except httpx.HTTPError as exc:
                last_error = exc

                if attempt >= self.max_retries:
                    break

                time.sleep(self.retry_delay)

        raise SMSNetworkError(f"Failed to send SMS after retries: {last_error}")


class AsyncSMSClient(_BaseSMSClient):
    def __init__(
        self,
        api_key: str,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        base_url: str = DEFAULT_BASE_URL,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            api_key,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            base_url=base_url,
        )

        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
        )

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncSMSClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ) -> None:
        await self.aclose()

    async def send(self, to: str, message: str) -> SMSResponse:
        payload = self._build_payload(to, message)
        url = self._build_url()

        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.post(url, json=payload)
                parsed = self._parse_response(response)

                if not response.is_success:
                    raise SMSAPIError(
                        "SMS API returned a non-success response.",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                return parsed

            except httpx.HTTPError as exc:
                last_error = exc

                if attempt >= self.max_retries:
                    break

                await asyncio.sleep(self.retry_delay)

        raise SMSNetworkError(f"Failed to send SMS after retries: {last_error}")
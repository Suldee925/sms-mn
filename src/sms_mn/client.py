from __future__ import annotations

import asyncio
import time

import httpx

from .exceptions import SMSAPIError, SMSNetworkError, SMSValidationError
from .models import SMSResponse
from .providers.base import BaseSMSProvider
from .providers.unitel import UnitelProvider

DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_RETRY_DELAY = 0.5
USER_AGENT = "sms-mn/0.2.0"


class _BaseSMSClient:
    def __init__(
        self,
        *,
        provider: BaseSMSProvider | None = None,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
    ) -> None:
        if provider is None and api_key is None:
            raise SMSValidationError("Provide either `provider` or `api_key`.")

        if provider is not None and api_key is not None:
            raise SMSValidationError("Use either `provider` or `api_key`, not both.")

        if timeout <= 0:
            raise SMSValidationError("`timeout` must be greater than 0.")
        if max_retries < 0:
            raise SMSValidationError("`max_retries` must be 0 or greater.")
        if retry_delay < 0:
            raise SMSValidationError("`retry_delay` must be 0 or greater.")

        self.provider = provider or UnitelProvider(api_key=api_key or "")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay


class SMSClient(_BaseSMSClient):
    def __init__(
        self,
        *,
        provider: BaseSMSProvider | None = None,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            provider=provider,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

        self._owns_client = client is None
        self._client = client or httpx.Client(
            timeout=self.timeout,
            headers={
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
        method, url, headers, json_body = self.provider.build_request(to=to, message=message)

        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self._client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_body,
                )
                parsed = self.provider.parse_response(response)

                if not response.is_success:
                    raise SMSAPIError(
                        f"{self.provider.name} API returned a non-success response.",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                return parsed

            except httpx.HTTPError as exc:
                last_error = exc

                if attempt >= self.max_retries:
                    break

                time.sleep(self.retry_delay)

        raise SMSNetworkError(
            f"Failed to send SMS via {self.provider.name} after retries: {last_error}"
        )


class AsyncSMSClient(_BaseSMSClient):
    def __init__(
        self,
        *,
        provider: BaseSMSProvider | None = None,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            provider=provider,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            timeout=self.timeout,
            headers={
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
        method, url, headers, json_body = self.provider.build_request(to=to, message=message)

        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_body,
                )
                parsed = self.provider.parse_response(response)

                if not response.is_success:
                    raise SMSAPIError(
                        f"{self.provider.name} API returned a non-success response.",
                        status_code=response.status_code,
                        response_text=response.text,
                    )

                return parsed

            except httpx.HTTPError as exc:
                last_error = exc

                if attempt >= self.max_retries:
                    break

                await asyncio.sleep(self.retry_delay)

        raise SMSNetworkError(
            f"Failed to send SMS via {self.provider.name} after retries: {last_error}"
        )
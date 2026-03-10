import httpx
import pytest
import respx

from sms_mn import AsyncSMSClient, SMSAPIError, SMSClient, SMSNetworkError, SMSValidationError
from sms_mn.providers import MobicomProvider, UnitelProvider


@respx.mock
def test_send_success_unitel() -> None:
    route = respx.post("https://pn.unitel.mn/api/message/send/sms?enc=test-key").mock(
        return_value=httpx.Response(200, json={"success": True})
    )

    client = SMSClient(provider=UnitelProvider(api_key="test-key"))
    response = client.send("88111111", "hello")

    assert route.called
    assert response.ok is True
    assert response.status_code == 200
    assert response.data == {"success": True}
    assert response.provider == "unitel"


@respx.mock
def test_send_success_mobicom() -> None:
    route = respx.get(
        "https://example.com/sms?servicename=test&username=user&from=123456&to=88111111&msg=hello"
    ).mock(return_value=httpx.Response(200, text="OK"))

    client = SMSClient(
        provider=MobicomProvider(
            base_url="https://example.com/sms",
            servicename="test",
            username="user",
            sender="123456",
        )
    )

    response = client.send("88111111", "hello")

    assert route.called
    assert response.ok is True
    assert response.status_code == 200
    assert response.raw_text == "OK"
    assert response.provider == "mobicom"


@respx.mock
def test_send_raises_api_error() -> None:
    respx.post("https://pn.unitel.mn/api/message/send/sms?enc=test-key").mock(
        return_value=httpx.Response(400, json={"error": "bad request"})
    )

    client = SMSClient(provider=UnitelProvider(api_key="test-key"))

    with pytest.raises(SMSAPIError):
        client.send("88111111", "hello")


@respx.mock
@pytest.mark.asyncio
async def test_async_send_success() -> None:
    route = respx.post("https://pn.unitel.mn/api/message/send/sms?enc=test-key").mock(
        return_value=httpx.Response(200, json={"success": True})
    )

    client = AsyncSMSClient(provider=UnitelProvider(api_key="test-key"))
    response = await client.send("88111111", "hello")
    await client.aclose()

    assert route.called
    assert response.ok is True
    assert response.provider == "unitel"


@respx.mock
def test_network_error_after_retries() -> None:
    respx.post("https://pn.unitel.mn/api/message/send/sms?enc=test-key").mock(
        side_effect=httpx.ConnectTimeout("timeout")
    )

    client = SMSClient(
        provider=UnitelProvider(api_key="test-key"),
        max_retries=1,
        retry_delay=0,
    )

    with pytest.raises(SMSNetworkError):
        client.send("88111111", "hello")


def test_validation_error_for_empty_message() -> None:
    client = SMSClient(provider=UnitelProvider(api_key="test-key"))

    with pytest.raises(SMSValidationError):
        client.send("88111111", "   ")


def test_legacy_api_key_still_works() -> None:
    client = SMSClient(api_key="legacy-test-key")
    assert client.provider.name == "unitel"
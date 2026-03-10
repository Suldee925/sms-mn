from sms_mn.providers import MobicomProvider


def test_mobicom_build_request() -> None:
    provider = MobicomProvider(
        base_url="YOUR_MOBICOM_BASE_URL",
        servicename="YOUR_SERVICE_NAME",
        username="YOUR_USERNAME",
        sender="YOUR_SENDER_NUMBER",
    )

    method, url, headers, json_body = provider.build_request(
        to="99112233",
        message="hello world",
    )

    assert method == "GET"
    assert "YOUR_MOBICOM_BASE_URL?" in url
    assert "servicename=YOUR_SERVICE_NAME" in url
    assert "username=YOUR_USERNAME" in url
    assert "from=YOUR_SENDER_NUMBER" in url
    assert "to=99112233" in url
    assert "msg=hello+world" in url
    assert headers == {}
    assert json_body is None
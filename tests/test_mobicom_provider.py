from sms_mn.providers import MobicomProvider


def test_mobicom_build_request() -> None:
    provider = MobicomProvider(
        servicename="mms",
        username="engineering",
        sender="139562",
    )

    method, url, headers, json_body = provider.build_request(
        to="88111111",
        message="hello world",
    )

    assert method == "GET"
    assert "http://27.123.214.168/smsmt/mt?" in url
    assert "servicename=mms" in url
    assert "username=engineering" in url
    assert "from=139562" in url
    assert "to=88111111" in url
    assert "msg=hello+world" in url
    assert headers == {}
    assert json_body is None
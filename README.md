# sms-mn

Production-ready Python client for sending SMS in Mongolia.

`sms-mn` нь Монголын SMS gateway-уудтай (Unitel, Mobicom) холбогдож мессеж илгээхэд зориулсан Python library юм.  
Provider pattern ашигласан тул өөр операторуудыг нэмэхэд маш хялбар.

---

## Supported Providers

- Unitel Premium Number API
- Mobicom HTTP SMS API

Цаашид дараах операторуудыг нэмэх боломжтой:

- Skytel
- Gmobile

---

## Install

```bash
pip install sms-mn
```

---

## Quick Start

### Unitel SMS илгээх

```python
from sms_mn import SMSClient, UnitelProvider

client = SMSClient(
    provider=UnitelProvider(
        api_key="YOUR_UNITEL_API_KEY",
    )
)

response = client.send(
    to="88112233",
    message="Hello from sms-mn via Unitel"
)

print(response)
client.close()
```

---

### Mobicom SMS илгээх

```python
from sms_mn import SMSClient, MobicomProvider

client = SMSClient(
    provider=MobicomProvider(
        servicename="mms",
        username="engineering",
        sender="139562",
    )
)

response = client.send(
    to="99112233",
    message="Hello from sms-mn via Mobicom"
)

print(response)
client.close()
```

---

## Async Usage

```python
import asyncio
from sms_mn import AsyncSMSClient, UnitelProvider

async def main():
    client = AsyncSMSClient(
        provider=UnitelProvider(api_key="YOUR_API_KEY")
    )

    response = await client.send(
        to="88112233",
        message="async sms"
    )

    print(response)

    await client.aclose()

asyncio.run(main())
```

---

## Response Object

`send()` функц дараах `SMSResponse` object буцаана.

```python
SMSResponse(
    ok=True,
    status_code=200,
    data={"success": True},
    raw_text="...",
    provider="unitel"
)
```

### Fields

| Field | Description |
|------|-------------|
| ok | Request амжилттай эсэх |
| status_code | HTTP response code |
| data | JSON response |
| raw_text | Raw response |
| provider | Ашигласан provider |

---

## Error Handling

Library дараах exception-уудыг ашигладаг.

```python
from sms_mn import (
    SMSValidationError,
    SMSAPIError,
    SMSNetworkError
)
```

Example:

```python
try:
    client.send("99112233", "hello")
except SMSValidationError:
    print("Invalid input")
except SMSAPIError:
    print("SMS API error")
except SMSNetworkError:
    print("Network problem")
```

---

## Project Structure

```
sms-mn
│
├─ src/
│  └─ sms_mn/
│     ├─ client.py
│     ├─ models.py
│     ├─ exceptions.py
│     ├─ utils.py
│     └─ providers/
│        ├─ base.py
│        ├─ 
..py
│        └─ mobicom.py
│
├─ tests/
├─ examples/
└─ README.md
```

---

## Development

Clone repository:

```bash
git clone https://github.com/Suldee925/sms-mn
cd sms-mn
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e .
```

---

## Run Tests

```bash
pytest
```

---

## Build Package

```bash
python -m build
```

---

## Publish to PyPI

```bash
twine upload dist/*
```

---

## Future Roadmap

Төлөвлөсөн feature-үүд:

- Bulk SMS
- OTP helper
- Delivery status
- Webhook receiver
- Skytel provider
- Gmobile provider

---

## License

MIT License

---

## Author

Created by **Suld-Erdene Erdenebat**

GitHub  
https://github.com/Suldee925
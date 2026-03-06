# sms-mn

Reusable Python SMS library for Mongolian telecom providers.

Supports sending SMS through telecom APIs such as:

- Unitel
- Mobicom (planned)
- Skytel (planned)

The library provides a clean interface for backend applications to send SMS notifications, OTP codes, alerts, and more.

---

## Installation

```bash
pip install sms-mn

from sms_mn import SMSClient

client = SMSClient.from_unitel(api_key="YOUR_API_KEY")

client.send(
    to="99112233",
    message="Hello from sms-mn"
)
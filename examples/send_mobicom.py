from sms_mn import MobicomProvider, SMSClient

client = SMSClient(
    provider=MobicomProvider(
        servicename="mms",
        username="engineering",
        sender="139562",
    )
)

response = client.send(
    to="99112233",
    message="Hello from sms-mn via Mobicom",
)

print(response)
client.close()
from sms_mn import SMSClient, UnitelProvider

client = SMSClient(
    provider=UnitelProvider(
        api_key="YOUR_UNITEL_API_KEY",
    )
)

response = client.send(
    to="99112233",
    message="Hello from sms-mn via Unitel",
)

print(response)
client.close()
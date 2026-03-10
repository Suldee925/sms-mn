from sms_mn import SMSClient, MobicomProvider

client = SMSClient(
    provider=MobicomProvider(
        base_url="YOUR_MOBICOM_BASE_URL",
        servicename="YOUR_SERVICE_NAME",
        username="YOUR_USERNAME",
        sender="YOUR_SENDER_NUMBER",
    )
)

response = client.send(
    to="99112233",
    message="Hello from sms-mn via Mobicom"
)

print(response.raw_text)
client.close()
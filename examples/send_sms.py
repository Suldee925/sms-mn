from sms_mn import SMSClient

client = SMSClient(api_key="YOUR_API_KEY")

response = client.send(
    to="88111111",
    message="Tanii OTP: 123456",
)

print(response)
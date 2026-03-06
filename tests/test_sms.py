from sms_mn import SMSClient

client = SMSClient.from_unitel("YOUR_API_KEY")

client.send(
    to="88112233",
    message="Test SMS"
)
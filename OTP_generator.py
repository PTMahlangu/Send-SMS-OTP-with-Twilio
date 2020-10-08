
import requests
import json
from  requests.exceptions import HTTPError
from twilio.rest import Client

account_sid = 'ACbd7508e59912ab391'
auth_token = ''
twilio_client = Client(account_sid, auth_token)

def generate_otp(phone_number):
    """ phone_number = identifier for the user requesting for the OTP code. """

    url ="https://api.generateotp.com/generate"
    data={'initiator_id': phone_number}
    response = requests.post(url,data)

    if response.status_code == 201:
        data = response.json()
        otp_code = str(data["code"])
        return otp_code


def verify_otp_code(otp_code, phone_number):
    r = requests.post(f"https://api.generateotp.com//validate/{otp_code}/{phone_number}")
    if r.status_code == 200:
        data = r.json()
        status = data["status"]
        message = data["message"]
        return status, message
    return None, None


def send_otp_via_sms(number, code):
    messages = twilio_client.messages.create(
        to=f"{number}", 
        from_='+***********', 
        body=f"Your one time password is {code}"
        )
    print(messages.sid)


def split_code(code):
    return " ".join(code)


def send_otp_via_voice_call(number, code):
    outline_code = split_code(code)
    call = twilio_client.calls.create(
        twiml=f"<Response><Say voice='alice'>Your one time password is {outline_code}</Say><Pause length='1'/><Say>Your one time password is {outline_code}</Say><Pause length='1'/><Say>Goodbye</Say></Response>",
        to=f"{number}",
        from_='+***********'
    )


if __name__ == "__main__":

    otp_code =generate_otp("+27**08****")
    print(otp_code)

    send_otp_via_sms("+27***08****", otp_code)


import requests
import time
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

def Ping(url, healthCheckTime, From, to):

    ping_cnt = 0

    while True:
        response = requests.get(url)

        if response.status_code == 200:
            ping_cnt = 0
            print(f"{url} is up!")

        elif ping_cnt > 3:
            HandlePingDownMessage(url, From, to)
            HandlePingDownCall(From, to)
            time.sleep(600)

        else:
            ping_cnt += 1
            print(f"{url} is down!")

        time.sleep(healthCheckTime)



def HandlePingDownCall(from_user, to_user, text_body):
    # use env variables
    account_sid = ""
    auth_token = ""

    client = Client(account_sid, auth_token)

    to_number = to_user
    from_number = from_user
    text_to_say = "YOUR WEBSITE IS DOWN"

    response = VoiceResponse()
    response.say(text_to_say)

    try:
        call = client.calls.create(
            twiml=str(response),
            to=to_number,
            from_=from_number
        )
        print("Call initiated successfully!")
    except Exception as e:
        print(f"Error making call: {e}")


# all parameter are passes as string
def HandlePingDownMessage(url, From, to):

    account_sid = "" #Enter twilio account_sid and auth_token
    auth_token = ""

    client = Client(account_sid, auth_token)
    to_number = to
    from_number = From

    message = f"{url} is down!"
    try:
        message = client.messages.create(
            to=to_number, from_=from_number, body=message)
        print("SMS sent successfully!")
        print(message.sid)
    except Exception as e:
        print(f"Error sending SMS: {e}")




if __name__ == "__main__":
    url = input('ENTER THE URL OF THE WEBSITE')
    healthCheckTime = int(
        input('ENTER THE TIME( IN SECONDS ) YOU WANT TO REPEAT HEALTH CHECK'))
    from_user = input('ENTER THE TWILIO SENDING MOBILE NUMBER')
    to_user = input("ENTER THE PHONE NUMBER YOU WANT TO RECIEVE THE ALERT")
    Ping("https://www.adaye.in/", healthCheckTime, from_user, to_user)

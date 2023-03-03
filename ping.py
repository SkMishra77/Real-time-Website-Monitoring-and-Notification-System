import requests
from decouple import config
import time
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

def Ping(url, healthCheckTime, From, to):
    """
    It checks if a website is up or down, and if it's down, it sends a text message and makes a phone
    call to the specified phone number
    
    :param url: The URL of the website you want to ping
    :param healthCheckTime: How often you want to check the URL
    :param From: The phone number that will be sending the text message
    :param to: The phone number you want to send the text message to
    """

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



def HandlePingDownCall(url, from_user, to_user, text_body):
    """
    This function will make a call to the number you specify, and say the text you specify
    
    :param from_user: The number you want to call from
    :param to_user: The phone number you want to call
    :param text_body: The text body of the message that was sent to the Twilio number
    """
    # use env variables
    account_sid = config('ACCOUNT_SID')
    auth_token = config('AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    to_number = to_user
    from_number = from_user
    text_to_say = f"YOUR WEBSITE {url} IS DOWN"

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
    """
    This function takes in a url, a from number, and a to number, and sends a text message to the to
    number saying that the url is down
    
    :param url: The URL to be monitored
    :param From: This is the Twilio number that you will be sending the SMS from
    :param to: The phone number you want to send the message to
    """

    account_sid = config('account_sid')
    auth_token = config('auth_token')

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
    Ping(url, healthCheckTime, from_user, to_user)

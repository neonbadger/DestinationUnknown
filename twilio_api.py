import io
import json
from twilio.rest import TwilioRestClient 

with io.open('config_twilio_secret.json') as cred:
    creds = json.load(cred)
    ACCOUNT_SID = creds['ACCOUNT_SID']
    AUTH_TOKEN = creds['AUTH_TOKEN']

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def send_uber_text():
    client.messages.create(
        to="+12039803811",
        from_="+12036803769", 
        body="Hi Shijie! Your Uber is en route! Your driver John (4.9 stars) will pick you up in 4 minutes.", 
        media_url="https://d1a3f4spazzrp4.cloudfront.net/uberex-sandbox/images/driver.jpg",
    )

    print "success"
    return "success"

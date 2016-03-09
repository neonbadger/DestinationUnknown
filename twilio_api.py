"""Twilio API setup and text messaging"""

import io
import json
import phonenumbers
import twilio
from twilio.rest import TwilioRestClient

with io.open('config_twilio_secret.json') as cred:
    creds = json.load(cred)
    ACCOUNT_SID = creds['ACCOUNT_SID']
    AUTH_TOKEN = creds['AUTH_TOKEN']
    TWILIO_NUMBER = creds['TWILIO_NUMBER']


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


def convert_to_e164(raw_phone):
    """Clean up phone numbers to E.164 format for Twilio API.

        >>> convert_to_e164('1234567890')
        u'+1234567890'

        >>> convert_to_e164('(123)456-7890')
        u'+1234567890'

        >>> convert_to_e164('123.456.7890')
        u'+1234567890'

    """

    if raw_phone[0] == '+':
        parse_type = None
    else:
        # If no country code, assume it's a US number
        parse_type = 'US'

    phone_representation = phonenumbers.parse(raw_phone, parse_type)

    return phonenumbers.format_number(phone_representation,
                                      phonenumbers.PhoneNumberFormat.E164)


def send_uber_text(phone_number="+12039803811"):
    """Send text message after Uber is called."""

    body = ("Hi Shijie! Your Uber is en route!"
            "Your driver John (4.9 stars) will pick you up in 4 minutes.")

    media_url = "https://d1a3f4spazzrp4.cloudfront.net/uberex-sandbox/images/driver.jpg"

    try:
        client.messages.create(
            to=phone_number,
            from_=TWILIO_NUMBER,
            body=body,
            media_url=media_url,
        )

        print "success"
        return "success"

    except twilio.TwilioRestException as e:
        print e
        return "Error"

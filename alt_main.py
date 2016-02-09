from yaml import safe_dump
from utils import import_app_credentials

from flask import Flask
from flask import session as sesh
from flask import redirect
from flask import request, url_for
from flask import render_template

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from uber_rides.auth import AuthorizationCodeGrant

# from rauth import OAuth2Service

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

import socket
import json
import requests
import httplib
import os
import io

import urllib
import urllib2

from datetime import datetime
import parsedatetime as pdt
import time

app = Flask(__name__)
app.requests_session = requests.Session()
app.secret_key = os.urandom(24)



# import app credentials imported from the configuration file.
credentials = import_app_credentials()

auth_flow = AuthorizationCodeGrant(
    credentials.get('client_id'),
    credentials.get('scopes'),
    credentials.get('client_secret'),
    credentials.get('redirect_url'),
)

auth_url = auth_flow.get_authorization_url()


@app.route('/')
def index():
    """Show landing page."""

    return render_template('index.html')

@app.route('/authenticate')
def login():
    """ Check if the user is logged in or not. OAuth2.0"""

    # for debugging
    print auth_url

    return redirect(auth_url)

@app.route('/redirect-uri', methods=['GET'])
def redirect_uri():
    """Implement a callback to obtain the access token."""

    parameters = {
        'redirect_uri': 'http://localhost:5000/redirect-uri',
        'code': request.args.get('code'),
        'grant_type': 'authorization_code',
    }

    client_id = credentials.get('client_id')
    client_secret = credentials.get('client_secret')

    response = requests.post(
        'https://login.uber.com/oauth/token',
        auth = (
            client_id,
            client_secret
        ),
        data = parameters
    )

    sesh['access_token'] = response.json().get('access_token')
    
    return redirect('/dashboard')


with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)


@app.route('/dashboard')
def dashboard():
    
    if 'access_token' not in sesh:
        return redirect(url_for('index'))
    else:
        
        # return """Works!!!!"""
        return render_template('dboard.html')



@app.route('/generateYelp.json', methods = ['POST'])
def generateYelp():
    """Return top search result without identifying info"""

    address = request.form.get("address")
    radius = request.form.get("radius")
    phonenumber = request.form.get("phonenumber")
    activity = request.form.get("activity")

    params = {
        'term': activity,
        'sort': 2,
        'radius_filter': int(radius)*1609.34,
    }

    location = address.split(" ")[-1]

    response = client.search(location, **params)

    biz = response.businesses[0]

    return render_template('yelp_result.html', biz = biz)


if __name__ == "__main__":
    
    # credentials = import_app_credentials()

    app.run(debug = True)


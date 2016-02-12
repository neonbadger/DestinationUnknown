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

from utils import import_oauth2_credentials
from uber_rides.session import OAuth2Credential

from rauth import OAuth2Service

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# import socket
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

import random
import pdb


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

credentials2 = import_oauth2_credentials()


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
    print 'access_token:', sesh['access_token']
    # access_token = sesh['access_token']
    
    return redirect('/dashboard')


with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    yelp_client = Client(auth)


@app.route('/dashboard')
def dashboard():
    
    if 'access_token' not in sesh:
        return redirect(url_for('index'))
    else:   
        # return """Works!!!!"""
        print sesh['access_token']

        return render_template('dboard.html')



@app.route('/generateYelp.json', methods = ['POST'])
def generateYelp():
    """Return top search result without identifying info"""

    address = request.form.get("address")
    radius = request.form.get("radius")
    phonenumber = request.form.get("phonenumber")
    activity = request.form.get("activity")

    group_activity = ['arcades', 'amusementparks', 'lasertag', 'rock_climbing', 'gokarts',
                      'escapegames', 'mini_golf', 'trampoline', 'zoos', 'bowling']

    fitness_activity = ['yoga', 'pilates', 'hiking', 'cyclingclasses']

    relax_activity = ['spas', 'hair', 'skincare', 'othersalons', 'massage',
                      'outlet_stores', 'shoppingcenters', 'massage_therapy',
                      'acupuncture', 'ayurveda', 'chiropractors', 'galleries', 
                      'gardens', 'museums', 'paintandsip', 'beaches']

    night_activity = ['cabaret', 'cinema', 'musicvenues', 'opera', 'theater',
                      'cocktailbars', 'lounges', 'sportsbars', 'wine_bar',
                      'poolhalls', 'pianobars', 'karaoke', 'jazzandblues',
                      'danceclubs']

    eat_activity = ['wineries', 'farmersmarket', 'bakeries', 'bubbletea', 'coffee',
                    'icecream', 'gourmet', 'juicebars', 'desserts', 'breweries']


    if activity == 'group':
        category_filter = random.choice(group_activity)
    elif activity == 'fitness':
        category_filter = random.choice(fitness_activity)
    elif activity == 'relax':
        category_filter = random.choice(relax_activity)
    elif activity == 'night':
        category_filter = random.choice(night_activity)
    elif activity == 'food':
        category_filter = random.choice(eat_activity)

    params = {
        # 'sort': 2,
        'radius_filter': int(radius)*1609.34,
        'category_filter': category_filter
    }

    response = yelp_client.search(address, **params)

    biz = response.businesses[0]

    print "access_token222", sesh.get('access_token')

    # credentials2 = import_oauth2_credentials()
    
    # oauth2credential = OAuth2Credential(
    #             client_id=credentials2.get('client_id'),
    #             access_token=sesh.get('access_token'),
    #             expires_in_seconds=credentials2.get('expires_in_seconds'),
    #             scopes=credentials2.get('scopes'),
    #             grant_type=credentials2.get('grant_type'),
    #             redirect_url=credentials2.get('redirect_url'),
    #             client_secret=credentials2.get('client_secret'),
    #             refresh_token=credentials2.get('refresh_token'),
    #         )

    # uber_session = Session(oauth2credential=oauth2credential)

    # uber_client = UberRidesClient(uber_session)

    # credentials2 = uber_session.oauth2credential

    # PRODUCT_ID = 'a1111c8c-c720-46c3-8534-2fcdd730040d'

    # # California Academy of Sciences
    # START_LAT = 37.770
    # START_LNG = -122.466

    # # Pier 39
    # END_LAT = 37.791
    # END_LNG = -122.405

    # estimate = uber_client.estimate_ride(
    #         PRODUCT_ID,
    #         START_LAT,
    #         START_LNG,
    #         END_LAT,
    #         END_LNG,
    #     )

    # print uber_client.get_products(37.77, -122.41)

    return render_template('yelp_result.html', biz = biz)

# print out access token for debugging
@app.route('/demo', methods=['GET'])
def demo():
    """Demo.html is a template that calls the other routes in this example."""
    
    token = sesh['access_token']
    print "access_token demo page1", sesh.get('access_token')
    print "access_token demo page", token

    return render_template('demo.html', token=token)

@app.route('/request_uber', methods=['GET', 'POST'])
def request_uber():
    """ """

    credentials2 = import_oauth2_credentials()
    
    oauth2credential = OAuth2Credential(
                client_id=credentials2.get('client_id'),
                access_token=sesh.get('access_token'),
                expires_in_seconds=credentials2.get('expires_in_seconds'),
                scopes=credentials2.get('scopes'),
                grant_type=credentials2.get('grant_type'),
                redirect_url=credentials2.get('redirect_url'),
                client_secret=credentials2.get('client_secret'),
                refresh_token=credentials2.get('refresh_token'),
            )

    # pdb.set_trace()

    uber_session = Session(oauth2credential=oauth2credential)

    uber_client = UberRidesClient(uber_session, sandbox_mode=True)

    credentials2 = uber_session.oauth2credential

    print "credentials2:", credentials2

    response = uber_client.get_products(37.77, -122.41)

    products = response.json.get('products')

    product_id = products[0].get('product_id')

    print product_id

    print uber_client.get_user_profile().json

    # response = uber_client.request_ride(product_id, 37.77, -122.41, 37.79, -122.41)
    
    # ride_details = response.json

    # print ride_details
    
    # ride_id = ride_details.get('request_id')

    # print ride_id

    return "success!"




if __name__ == "__main__":
    
    # credentials = import_app_credentials()


    app.run(debug = True)


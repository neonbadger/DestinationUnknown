from yaml import safe_dump

from flask import Flask
from flask import session as sesh
from flask import redirect
from flask import request, url_for
from flask import render_template
from flask import flash, jsonify

from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.session import OAuth2Credential
from utils import import_app_credentials
from utils import import_oauth2_credentials

# from rauth import OAuth2Service

from yelp_api import yelp_random_pick
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from model import connect_to_db, db, User, Search, Rating

import requests
import os

import httplib
import urllib
import urllib2

from datetime import datetime
import parsedatetime as pdt
import time

# import pdb

app = Flask(__name__)
app.requests_session = requests.Session()
app.secret_key = os.urandom(24)

geolocator = Nominatim()

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

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

    return render_template('index2.html')

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


@app.route('/dashboard')
def dashboard():
    
    if 'access_token' not in sesh:
        return redirect(url_for('index'))
    else:   
        # return """Works!!!!"""
        print sesh['access_token']

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

        uber_session = Session(oauth2credential=oauth2credential)
        uber_client = UberRidesClient(uber_session, sandbox_mode=True)

        print uber_client.get_user_profile().json

        user_profile = uber_client.get_user_profile().json

        sesh['user'] = {
                        'first_name': user_profile.get('first_name'),
                        'last_name': user_profile.get('last_name'),
                        'email': user_profile.get('email'),
                        'phone': user_profile.get('phone'),
                        'img_url': user_profile.get('picture')
        }

        print sesh['user']

        if db.session.query(User).filter(User.email == user_profile['email']).count() == 0:
            user = User(first_name=user_profile.get('first_name'),
                        last_name= user_profile.get('last_name'),
                        img_url=user_profile.get('picture'),
                        email=user_profile.get('email'))
            db.session.add(user)
            db.session.commit()
        else:
            first_name = User.query.filter(User.email == user_profile['email']).first().first_name
            print "Hello!", first_name


        return render_template('dboard.html', 
                                first_name=sesh['user'].get('first_name'),
                                img_url=sesh['user'].get('img_url'),
                                )



@app.route('/yelp_result', methods = ['POST'])
def generateYelp():
    """Return top search result without identifying info"""

    mood = request.form.get('mood')
    adjective = request.form.get('adjective')
    alter_ego = request.form.get('alter_ego')

    location = request.form.get('location')
    start = geolocator.geocode(request.form.get('location'))
    start_lat = start.latitude
    start_lng = start.longitude

    event = request.form.get('event')
    city = request.form.get('city')
    phone = request.form.get('phone')

    biz = yelp_random_pick(event, city)
    end_lat = biz.location.coordinate.latitude
    end_lng = biz.location.coordinate.longitude

    distance = vincenty((start_lat, start_lng), (end_lat, end_lng)).miles

    sesh['user']['phone'] = phone
    user = User.query.filter(User.email == sesh['user'].get('email')).first()
    user_id = user.id
    if user.phone == None:
        user.phone = phone
        db.session.commit()

    search = Search(user_id=user_id,
                mood=mood,
                adjective=adjective,
                alter_ego=alter_ego,
                event=event,
                location=location,
                start_lat=start_lat,
                start_lng=start_lng,
                destination=biz.name,
                end_lat=end_lat,
                end_lng=end_lng,
                mileage=distance,
                )
    db.session.add(search)
    db.session.commit()

    print ("yelp stuff:", mood, adjective, alter_ego, location, start, start_lat, start_lng,
          event, city, phone, biz.categories)
    print ('end stuff:', end_lat, end_lng)
    # if refresh page on yelp search, access_token is lost
    print "access_token222", sesh.get('access_token')
    print sesh['user']

    return render_template('yelp_result.html', biz=biz,
                                               review=biz.snippet_text.replace('\n', ' '),
                                               pic = sesh['user'].get('img_url'),
                                               first_name=sesh['user'].get('first_name'),
                                               location=location,
                                               start_lat=start_lat,
                                               start_lng=start_lng,
                                               end_lat=end_lat,
                                               end_lng=end_lng,
                                               )

# print out access token for debugging
@app.route('/demo', methods=['GET'])
def demo():
    """Demo.html is a template that calls the other routes in this example."""
    
    token = sesh['access_token']
    print "access_token demo page1", sesh.get('access_token')
    print "access_token demo page", token

    return render_template('demo.html', token=token)

@app.route('/request_uber', methods=['POST'])
def request_uber():
    """ """

    search = Search.query.order_by(Search.date.desc()).first()
    search.uber_request = True
    db.session.commit()

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

    # receive data from the Ajax call
    start_lat = request.form.get('start_lat')
    start_lng = request.form.get('start_lng')
    end_lat = request.form.get('end_lat')
    end_lng = request.form.get('end_lng')

    print start_lat, start_lng, end_lat, end_lng

    response = uber_client.get_products(start_lat, start_lng)

    products = response.json.get('products')

    product_id = products[0].get('product_id')

    print product_id
    print "response", response.json
    print uber_client.get_user_profile().json
    print uber_client.get_user_activity().json

    ride_request = uber_client.request_ride(product_id, start_lat, start_lng, end_lat, end_lng)
    
    ride_details = ride_request.json

    print "ride details:", ride_details
    
    ride_id = ride_details.get('request_id')

    print ride_id

    get_ride = uber_client.update_sandbox_ride(ride_id, 'accepted')

    print get_ride

    return jsonify(products[0])


if __name__ == "__main__":
    
    # credentials = import_app_credentials()

    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    db.create_all()
    db.session.commit()

    app.run()


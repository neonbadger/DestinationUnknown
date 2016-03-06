from flask import Flask
from flask import session as sesh
from flask import redirect
from flask import request, url_for
from flask import render_template
from flask import jsonify

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.session import OAuth2Credential
from utils import import_app_credentials
from utils import import_oauth2_credentials

from yelp_api import yelp_random_pick
from twilio_api import send_uber_text

from geopy.geocoders import Nominatim
from geopy.distance import vincenty

from model import connect_to_db, db, User, Search
from sqlalchemy import func

import requests
import os


app = Flask(__name__)
app.requests_session = requests.Session()
app.secret_key = os.urandom(24)


geolocator = Nominatim()


# Step 1 in 3-legged OAuth handshake:
# Prepare OAuth 2.0 service that is used to make requests
credentials = import_app_credentials()

auth_flow = AuthorizationCodeGrant(
    credentials.get('client_id'),
    credentials.get('scopes'),
    credentials.get('client_secret'),
    credentials.get('redirect_url'),
)

# Generate authorization url
auth_url = auth_flow.get_authorization_url()



@app.route('/')
def index():
    """Show homepage."""

    return render_template('home.html')



@app.route('/authenticate')
def login():
    """Redirect to https://login.uber.com/login"""

    return redirect(auth_url)



@app.route('/redirect-uri', methods=['GET'])
def redirect_uri():
    """Step 2 & 3 in 3-legged Oauth handshake. Implement callback 
    at redirect_uri to exchange a code to obtain access token"""

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

    # Extract access token and store in session
    sesh['access_token'] = response.json().get('access_token')

    return redirect('/search')



@app.route('/search')
def search():
    """Show search form and create user object if not in database"""
    
    if 'access_token' not in sesh:
        return redirect(url_for('index'))
    else:
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

        user_profile = uber_client.get_user_profile().json

        sesh['user'] = {
                        'first_name': user_profile.get('first_name'),
                        'last_name': user_profile.get('last_name'),
                        'email': user_profile.get('email'),
                        'phone': user_profile.get('phone'),
                        'img_url': user_profile.get('picture')
        }

        # print sesh['user']

        if db.session.query(User).filter(User.email == user_profile['email']).count() == 0:
            user = User(first_name=user_profile.get('first_name'),
                        last_name= user_profile.get('last_name'),
                        img_url=user_profile.get('picture'),
                        email=user_profile.get('email'))

            db.session.add(user)
            db.session.commit()

        return render_template('search.html',
                                first_name=sesh['user'].get('first_name'),
                                img_url=sesh['user'].get('img_url'),
                                )



@app.route('/yelp_result', methods = ['POST'])
def generate_yelp():
    """Return top-rated Yelp search result and create search object in database"""

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



@app.route('/request_uber', methods=['POST', 'GET'])
def request_uber():
    """Make sandbox Uber ride request"""

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

    uber_session = Session(oauth2credential=oauth2credential)

    uber_client = UberRidesClient(uber_session, sandbox_mode=True)

    # receive data from Ajax call
    start_lat = request.form.get('start_lat')
    start_lng = request.form.get('start_lng')
    end_lat = request.form.get('end_lat')
    end_lng = request.form.get('end_lng')

    response = uber_client.get_products(37.3688301, -122.0363495)

    products = response.json.get('products')

    product_id = products[0].get('product_id')

    # make sandbox calls
    ride_request = uber_client.request_ride(product_id=product_id, 
                                            start_latitude=37.3688301, 
                                            start_longitude=-122.0363495, 
                                            end_latitude=37.8003415, 
                                            end_longitude=-122.4331332)
   
    ride_details = ride_request.json
  
    ride_id = ride_details.get('request_id')

    get_ride = uber_client.update_sandbox_ride(ride_id, 'accepted')

    send_uber_text();

    return jsonify(ride_details)



@app.route('/show_stats')
def show_stats():
    """Show user's boldness stats and D3 graphs"""

    bold_stat = Search.query.filter_by(uber_request = 'T').count()
    curious_stat = Search.query.filter_by(uber_request = 'F').count()
    uber_miles = db.session.query(func.sum(Search.mileage)).filter(Search.uber_request == 'T').scalar()

    moods = db.session.query(func.count(Search.mood), Search.mood).group_by(Search.mood).all()
    alter_ego = db.session.query(func.count(Search.alter_ego), Search.alter_ego).group_by(Search.alter_ego).all()

    # print moods, alter_ego

    return render_template("stats.html", 
                            bold_stat=bold_stat,
                            curious_stat=curious_stat,
                            uber_miles=uber_miles)



@app.route('/check_token', methods=['GET'])
def check_access_token():
    """A test route that checks whether access token is fresh."""
    
    token = sesh['access_token']

    return render_template('check_token.html', token=token)



if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    db.create_all()
    db.session.commit()

    app.run()
    url_for('static', filename='event.csv')

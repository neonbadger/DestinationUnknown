import io
import json
import random

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    yelp_client = Client(auth)

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

def yelp_random_pick(event, city):
    """Generates top pick for users."""

    if event == 'food':
        category_filter = random.choice(eat_activity)
    elif event == 'friends':
        category_filter = random.choice(group_activity)
    elif event == 'relax':
        category_filter = random.choice(relax_activity)
    elif event == 'nightlight':
        category_filter = random.choice(night_activity)
    elif event == 'fitness':
        category_filter = random.choice(fitness_activity)

    params = {
        'sort': 2,
        # 'radius_filter': int(radius)*1609.34,
        'category_filter': category_filter
    }

    response = yelp_client.search(city, **params)

    biz = response.businesses[0]

    return biz
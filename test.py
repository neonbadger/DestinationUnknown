"""Test suite for Destination Unknown app"""

import unittest
import doctest
import server
from server import app
from model import db
from model import User, Search, Rating
from twilio_api import convert_to_e164, send_uber_text


# Doctest

def load_tests(loader, tests, ignore):
    """Run doctests and file-based doctests."""

    tests.addTests(doctest.DocTestSuite(server))
    return tests


#Test Database

class ModelTests(unittest.TestCase):
    """Tests for database"""

    def setUp(self):
        """Set up database for testing purposes"""

        print "Setting up test database"
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = app
        db.init_app(app)
        db.create_all()

    def _create_user(self):

        user = User(first_name='Jane', last_name='Doe', img_url='',
                    email='jane.doe@test.com', phone='1234567890')
        db.session.add(user)
        db.session.commit()

    def _create_search(self):

        user = User.query.filter_by(first_name='Jane').first()

        search = Search(user_id=user.id, mood='anxious', adjective='epic',
                        alter_ego='TSwift', event='eat', location='San Francisco',
                        start_lat=37, start_lng=-122, destination='Ferry Building',
                        end_lat=37, end_lng=-122, mileage=5, uber_request=True)

        db.session.add(search)
        db.session.commit()

    def _create_rating(self):

        user = User.query.filter_by(first_name='Jane').first()
        search = Search.query.filter_by(destination='Ferry Building').first()

        rating = Rating(search_id=search.id, user_id=user.id, user_rating=5, 
                        user_comment="Excellent! Would totally do it again!")

    def test_query_user(self):

        self._create_user()
        self._create_search()
        self._create_rating()
        expected = User.query.filter_by(first_name='Jane').first()
        result = User.query.get(1)
        self.assertEqual(result, expected)

    def test_query_search(self):
       
        expected = Search.query.filter_by(uber_request=True).first()
        result = Search.query.get(1)
        self.assertEqual(result, expected)

    def test_query_rating(self):
       
        expected = Rating.query.filter_by(user_rating=5).first()
        result = Rating.query.get(1)
        self.assertEqual(result, expected)

    def tearDown(self):
        """Remove testing db"""

        db.session.remove()
        db.drop_all()
        print "teardown ran"


# Test Twilio

class TwilioUnitTestCase(unittest.TestCase):
    """Unit tests on Twilio SMS and phone number conversion"""

    def test_convert_to_e164(self):
        """Test phone number conversion"""

        self.assertEqual(convert_to_e164('1234567890'), u'+1234567890')

    def test_convert_to_e164_plus(self):
        """Test phone number conversion with + sign"""

        self.assertEqual(convert_to_e164('+1234567890'), u'+1234567890')

    def test_convert_to_e164_parens(self):
        """Test phone number conversion with ()"""

        self.assertEqual(convert_to_e164('(123)456-7890'), u'+1234567890')

    def test_convert_to_e164_period(self):
        """Test phone number conversion with ."""

        self.assertEqual(convert_to_e164('123.456.7890'), u'+1234567890')

    def test_convert_to_e164_dash(self):
        """Test phone number conversion with -"""

        self.assertEqual(convert_to_e164('123-456-7890'), u'+1234567890')

    def test_send_uber_text(self):
        """Test SMS with uber ride information"""

        self.assertEqual(send_uber_text('+1203983811'), "success")

    def test_send_uber_text(self):
        """Test SMS with invalid phone number"""

        self.assertEqual(send_uber_text('+1234567890'), "Error")



#Test Flask

class FlaskTests(unittest.TestCase):
    """Integration tests on Flask server"""

    def setUp(self):
        """Set up Flask app for testing"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):

        # integration tests
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn("<span class='special'>Find Your Destination Unknown</span>", result.data)

    # def test_demo(self):

    #     result = self.client.get('/demo')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])

    # def test_stats(self):

    #     result = self.client.get('/show_stats')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('View Your Stats', result.data)


# Selenium Test

from selenium import webdriver
from time import sleep

class TestUberLogin(unittest.TestCase):
    """Test Uber login button redirects to Uber login page"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_uber_login(self):
        self.browser.get("http://localhost:5000")
        sleep(1)
        button = self.browser.find_element_by_id('btn')
        action = webdriver.ActionChains(self.browser)
        action.move_to_element(button)
        action.perform()
        login_button = self.browser.find_element_by_id('login')
        login_button.click()
        sleep(5)
        # import pdb; pdb.set_trace()
        redirect_url = self.browser.current_url
        expected_url = "https://login.uber.com/login"
        
        self.assertEqual(expected_url, redirect_url)

if __name__ == '__main__':

    unittest.main()

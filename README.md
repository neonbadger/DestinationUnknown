![Destination Unknown Logo](/static/img/Question_Mark_3.png "Destination Unknown Logo")

**Destination Unknown** is a mischievous roulette mystery trip generator that can sweep you away on a spontaneous adventure. Users can log in with their Uber accounts, compose a story for their ideal escape, and see a top-rated mystery destination unfold on a story-book map. The destination contains just enough information to pique one’s interest but not spoil the surprise. Users can request a ride from Uber directly via Destination Unknown, complete with text message confirmation. Destination Unknown also provides users with insights into their own “Inside Out”: curiosity stats, mood triggers, and celebrity alter-egos. 

As the saying goes, “*Only the curious have something to find*.” Destination Unknown will encourage you to forge a bolder path.

Destination Unknown web app and logo are created with love by **Shijie Feng** <shijie.feng@gmail.com>. You can connect with Shijie on [LinkedIn](https://www.linkedin.com/in/shijiefeng), [Twitter](https://twitter.com/Neon_Badger), [Medium](https://medium.com/@ShijieF).


# Table of Contents
* [Technologies](#technologies)
* [Features](#features)
* [Intallation](#install)
* [Testing](#testing)
* [Deployment](#deployment)
* [Version 2.0](#future)
* [Author](#author)
* [License](#license)
* [Acknowledgment](#acknowledgment)


## <a name="technologies"></a>Technologies

**Destination Unknown** is built on a Flask server (written in Python) and uses a PostgreSQL database. The application seamlessly integrates with Uber, Yelp, Mapbox, and Twilio APIs and adopts a modernized UI that supports full-screen video background, natural language form, and JavaScript/jQuery/CSS animation effects. While using Destination Unknown, users generate live data, and the application queries the database and visualizes the information with jQuery and D3.js.

Tech Stack:
* Frontend: JavaScript, [jQuery](https://jquery.com/), [AJAX](http://api.jquery.com/jquery.ajax/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [D3.js](https://d3js.org/), [Bootstrap](http://getbootstrap.com/2.3.2/), [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)
* Backend: [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/)
* Database: [Flask - SQLAlchemy](http://flask.pocoo.org/), [PostgreSQL](http://www.postgresql.org/)
* API: [Uber](https://developer.uber.com/), [Yelp](https://www.yelp.com/developers/documentation/v2/overview), [Mapbox](https://www.mapbox.com/developers/), [Twilio](https://www.twilio.com/docs/api/rest)

(Dependencies are listed in [requirements.txt](requirements.txt).)

## <a name="features"></a>Features

####Full-Screen Video Background
![](/static/img/Landing_1.gif)

The landing page embeds HTML5 video in the background for a stunning, fluid user experience. The video background is supported in all modern browsers (>IE8). For browsers incompatible with HTML5 video, a static full-screen picture is shown instead.

I create my own video for the app's background. To make the video background work on the web, I host three formats:
* MP4 – a container for H.264 video and AAC audio
* Ogg – a container for Theora video and Vorbis audio
* WebM – a container intended primarily for use in the HTML5 video tag

####Login with Uber

When the mouse hovers to the center of the landing page, a hidden login button appears. I opt for this "hide-and-seek" button effect to augment the app's "*Be Curious, Be Bold*" message.

User login is handled through Uber's OAuth 2.0, following the client-side authorization flow. 
![](/static/img/Login_2.gif)

* _What does Destination Uknown's OAuth flow look like?_

For a user to access Destination Unknown's content and request in-app Uber services, the app needs authorization from Uber and redirects the user to Uber's Authorization server, where the user is asked to authenticate (if not already logged in) and then authorize the requested permissions. After successfully being granted access, the app is redirected from Uber to the redirect uri address, including an access token that can be used directly by the app to request information or perform operations on behalf of the user. 

The access token is then encrypted and stored on the Flask session, and the user's subsequent login will not prompt for the authorization dialog if the user is logged in and has previously approved the same permissions. For more, please see the [Uber API documentation](https://developer.uber.com/docs/authentication).

####User Profile and Avatar

Upon a user's successful login through Uber, the app accesses the user's Uber profile and greets the user with the user's name and Uber profile picture on top of the search page. With a mouseover, you can turn into a curious cat!
![](/static/img/Avatar_1.gif)

####Natural Language User Interface

Destination Unknown experiments with a novel UI concept to transform the conventional Q&A-style forms for user input. The app implements a Natural Language Form ("NLF"), embedding input fields inside sentences to make filling out a form as engaging and as writing a mini story, and as easy as talking to a friend. 

In addition to asking for the user's current location, desired activity type, and preferred destination, the form collects the user's mood information at the time of search by asking about the user's feeling, self-description, and celebrity alter-ego. For more design inspirations on NLF, please visit this [blog](http://www.jroehm.com/2014/01/ui-pattern-natural-language-form/).
![](/static/img/NLP_Form_1.gif)

####Business Discovery

Destination Unknown uses the Yelp API behind the scene to determine the list of businesses to choose from. Once the user fills out the form and clicks the "Find Destination" button, the application sends the search parameters to Yelp API's search endpoint. After Yelp returns results that fit the search criteria, the app randomly selects one of the highest-rated businesses for the user's consideration, revealing only the business's Yelp ratings, review snippet, and business categories -- just enough information to get you curious and excited!
![](/static/img/Destination_1.gif)

####Story Book Map

The background map is composed of a Mapbox (built on Leaflet) map with custom markers and popups, custom CSS, Bootstrap, and jQuery. The theme of the map is a customized [picture book atlas](https://github.com/mapbox/mapbox-studio-picture-book.tm2) designed in Mapbox Studio. 

The map has a transparent nav bar overlay on top, displaying the user's phone number, current location, and a link to view the user's stats. The map shows two custom-made markers: one for the user with a popup window greeting the user and indicating the user's current location, and the other for the mystery destination with a popup window containing the selected business information

The user has the option of returning to the previous search page, or requesting Uber to Destination Unknown. 

####Uber Ride Request (sandbox)

A user can click "Call Uber" button and a modal window will appear. After confirming the ride request, the app sends an AJAX request to the Flask controller, sending along the geolocations of the user and the selected business. The app then uses the OAuth 2.0 credentials to instantiate a client object, makes a request to Uber's v1/requests endpoint that returns Uber products in the vincinity of the user, and picks a UberX (or UberXL if no UberX is available). The app makes a sandbox ride request to Uber, changing product status to "accepted." After Uber grants the ride request, Uber returns a successful 200 status code, and the app can access the ride details including the driver's name and rating, the vehicle's make and model, and the estimated pickup. The "Call Uber" button is disabled and turns into "Uber Called." For more, please visit [Uber API tutorial](https://developer.uber.com/docs/tutorials-rides-api).

![](/static/img/Call_Uber_2.gif)

####Twilio Text Message Confirmation

When the user's ride request is successful, the app sends the ride information to the user via the Twilio SMS API.

####Live User-Generated Data

As the user fills out the form, all the form fields -- including the user's mood, trip description, and alter-ego -- are written into the database, along with information about the destination generated by the application. When the user requests Uber, the uber_request field in the searches table is updated accordingly.

####Curiosity and Mood Stats Visualization

The app makes SQLAlchemy queries into the database and returns the following data: the number of times the user has been curious and searched for a destination (curiosity stats), the number of times the user has been bold and requested Uber (boldness stats), and how many miles the user has traveled to Destination Unknown with Uber (in sandbox). With jQuery, these stats are shown with a flipping countup animation effect.
![](/static/img/Stats_1.gif)

The user can also view a donut chart illustrating the percentage of times the user selected his or her celebrity alter-egos, made with D3.js. The user can selects and deselects the alter-ego in the legend to view the relative percentages.
![](/static/img/Donut_1.gif)
 
In addition, there is a chord diagram showing how the user's mood affects the activity choice, also made with D3.js. How does feeling anxious correspond to whether you eat out more or work out more? How does practicing zen relate to how you feel? Find out the answers here!

![](/static/img/Chord_2.gif)

## <a name="install"></a>Installation

If you want to get a copy of this project up and running on your local machine for development and testing purposes, follow the following steps.

####Prerequisite

Install PostgreSQL (Mac OSX)

Use Sublime to edit the file in your home directory named .bash_profile:

``` $ subl ~/.bash_profile ``` 

Then, at the bottom of this file, add the following line (exactly):

``` export PATH=/Applications/Postgres.app/Contents/Versions/9.4/bin/:$PATH ``` 


####Installing

Clone this repository.

```
$git clone https://github.com/neonbadger/DestinationUnknown.git
```
Create a virtual environment for the project.

```
$ virtualenv env
```
Activate the virtual environment.
```
$ source env/bin/activate
```
Install dependencies.
```
$ pip install -r requirements.txt
```
To enable the Uber, Yelp, and Twilio functionality, you should set up your own developer accounts and have your own sets of API keys and tokens. Examples of the config files are provided in the folder [config_example](config_example).

Run PostgreSQL.

Create database with the name 'trips.'
```
$ psql trips

$ dropdb trips

$ createdb trips
```
To run the app from the command line of the terminal, run
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i server.py
```

## <a name="testing"></a>Testing

Currently there is a test suite encompassing Unittest, Integration Test, and Selenium Test.

To run the tests on command line:
```
$ coverage run tests.py
```
For report:
```
$ coverage report -m server.py
```

## <a name="deployment"></a>Deployment

Add additional notes about how to deploy this on a live system

## <a name="future"></a>Version 2.0

Future features to come:

- [ ] Drag and drop the user's geolocation
- [ ] User rate and review the Destination Unknown post Uber trip
- [ ] Multiple legs of trip
- [ ] Incorporate machine learning to predict user's preference
- [ ] More testing

## <a name="author"></a>Author

**Shijie Feng** (Github: [neonbadger](https://github.com/neonbadger)) is a software engineer and lives in San Francisco Bay Area with her husband Blake and cat Mylo.

## <a name="license"></a>License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.

## <a name="acknowledgments"></a>Acknowledgments

* Hat tip to my wonderful husband Blake for love and support during Hackbright!
* Thanks to my mentors Terry, Sri, Monica, advisor Ally, and my Hack13right sisters for guidance and support!

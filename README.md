![Destination Unknown Logo](/static/img/question_mark_3.png "Destination Unknown Logo")

**Destination Unknown** is a mischievous roulette mystery trip generator that can sweep you away on a spontaneous adventure. Users can log in with their Uber accounts, compose a story for their ideal escape, and see a top-rated mystery destination unfold on a story-book map. The destination contains just enough information to pique one’s interest but not spoil the surprise. Users can request a ride from Uber directly via Destination Unknown, complete with text message confirmation. Destination Unknown also provides users with insights into their own “Inside Out”: curiosity stats, mood triggers, and celebrity alter-egos. 

As the saying goes, “*Only the curious have something to find*.” Destination Unknown will encourage you to forge a bolder path.

Destination Unknown web app and logo are created with love by **Shijie Feng**. You can connect with Shijie on [LinkedIn](https://www.linkedin.com/in/shijiefeng), [Twitter](https://twitter.com/Neon_Badger), and [Medium](https://medium.com/@ShijieF).


# Table of Contents
* [Technologies](#technologies)
* [Features](#features)
* [Testing](#testing)
* [Set Up](#setup)
* [Deployment](#deployment)
* [Future Features](#future)
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

When the mouse hovers to the center of the landing page, a hidden login button appears. I opt for a "hide-and-seek" button to augment the app's "*Be Curious, Be Bold*" message.

User login is handled through Uber's OAuth 2.0, following the client-side authorization flow. 
![](/static/img/Login_2.gif)

* What does Destination Uknown's OAuth flow look like?

For a user to access Destination Unknown's content and request in-app Uber services, the app needs to get authorization from Uber and redirect the user to Uber's Authorization server, where he or she is asked to authenticate (if not already logged in) and then authorize the requested permissions. After successfully being granted access, the application is redirected to the redirect_uri address, including an access_token that can be used directly by the app to request information or perform operations on behalf of the user. Access_token is then encrypted and stored on the Flask session, and the user's subsequent login will not prompt for the authorization dialog if the user is logged in and has previously approved the same permissions. For more, please see [Uber API documentation](https://developer.uber.com/docs/authentication).

####User Avatar

Upon a user's successful login through Uber, the app accesses the user's Uber profile and displays it on the search page. With a mouseover, you can turn into a curious cat!
![](/static/img/Avatar_1.gif)

####Natural Language User Interface

Destination Unknown experiments with a novel UI concept to transform the conventional Q&A-style forms for user input. The app implements a Natural Language Form ("NLF"), embedding input fields inside sentences to make filling out a form as engaging and as writing a mini story, and as easy as talking to a friend. In addition to asking for the user's current location, desired event type, and preferred destination, the form collects the user's feelings at the time of search by asking about the user's mood, self-description, and celebrity alter-ego. For more design inspirations on NLF, please visit this [blog](http://www.jroehm.com/2014/01/ui-pattern-natural-language-form/).
![](/static/img/NLP_Form_1.gif)

####Business Discovery

Destination Unknown uses the Yelp API behind the scene to determine the list of businesses to choose from. Once the user fills out the form and clicks the "Find Destination" button, the application sends the search parameters to Yelp API's search endpoint. After Yelp returns results that fit the search criteria, the app randomly selects one of the highest-rated businesses for the user's consideration, revealing only the business's Yelp ratings, review snippet, and business categories -- just enough information to get you curious and excited!
![](/static/img/Destination_1.gif)

####Story Book Map

The background map is composed of a Mapbox (built on Leaflet) map with custom markers and popups, custom CSS, Bootstrap, and jQuery. The theme of the map is a customized [picture book atlas](https://github.com/mapbox/mapbox-studio-picture-book.tm2) designed in Mapbox Studio. The map shows two custom-made markers: one for the user with a popup window greeting the user and indicating the user's current location, and the other for the mystery destination with a popup window containing the selected business information. The user has the option of returning to the previous search page, or requesting Uber to Destination Unknown.

####Uber Ride Request (sandbox)

A user can click "Call Uber" button and a modal window will appear. After confirming the ride request, the app sends an AJAX request to the Flask controller, sending along the geolocations of the user and the selected business. The app then uses the OAuth 2.0 credentials to instantiate a client object, makes a request to Uber's v1/requests endpoint that returns Uber products in the vincinity of the user, and picks a UberX (or UberXL if no UberX is available). The app makes a sandbox ride request to Uber, changing product status to "accepted." After Uber grants the ride request, Uber returns a successful 200 status code, and the app can access the ride details including the driver's name and rating, the vehicle's make and model, and the estimated pickup. The "Call Uber" button is disabled and turns into "Uber Called." For more, please visit [Uber Rides API tutorial](https://developer.uber.com/docs/tutorials-rides-api).
![](/static/img/Call_Uber_2.gif)

####Twilio Text Message Confirmation

When the user's ride request is successful, the app uses the Twilio SMS API to send the ride information to the user.

####Live User-Generated Data

As the user fills out the form, all the form fields -- including the user's mood, trip description, and alter-ego -- are written into the database, along with information about the destination generated by the application. When the user requests Uber, the uber_request field in the searches table is updated accordingly.

####Curiosity and Mood Stats Visualization

The app makes SQLAlchemy queries into the database and returns the following data: the number of times the user has been curious and searched for a destination (curiosity stats), the number of times the user has been bold and requested Uber (boldness stats), and how many miles the user has traveled to Destination Unknown with Uber (in sandbox). With jQuery, these stats are shown with a flipping countup animation effect. In addition, the user can also view a donut chart illustrating the percentage of times the user selected his or her celebrity alter-egos, and a chord diagram showing how the user's mood affects the activity choice on a chord diagram. Both interactive charts are made with D3.js.
![](/static/img/Stats_1.gif)
![](/static/img/Donut_1.gif)
![](/static/img/Chord_2.gif)

## <a name="testing"></a>Testing

The application has been tested with Unittest, integration test, and selenium.

## <a name="setup"></a>Set Up

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

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
To enable the Uber, Yelp, and Twilio functionality, you should have your own sets of API keys and tokens. Examples are provided in the folder [config_example](config_example).

Run PostgreSQL.

Create database with the name 'trips' and run model.py.
```
python -i model.py
```


#### Configuration



## <a name="testing"></a>Testing

Explain how to run the automated tests for this system

#### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

## <a name="deployment"></a>Deployment

Add additional notes about how to deploy this on a live system

## <a name="future"></a>Future Features
* Drag and drop the user's geolocation
* User rate and review the Destination Unknown post trip
* Improve search algorithm and incorporate machine learning to predict user's preference
* More testing

## <a name="author"></a>Author

**Shijie Feng** (Github: [neonbadger](https://github.com/neonbadger)) is a software engineer from San Francisco, CA.

## <a name="license"></a>License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## <a name="acknowledgments"></a>Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

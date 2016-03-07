# DESTINATION UNKNOWN

**Destination Unknown** is a mischievous roulette mystery trip generator that can sweep you away on a spontaneous adventure. Users can log in with their Uber accounts, compose a story for their ideal escape, and see a top-rated mystery destination unfold on a story-book map. The destination contains just enough information to pique one’s interest but not spoil the surprise. Users can request a ride from Uber directly via Destination Unknown, complete with text message confirmation. Destination Unknown also provides users with insights into their own “Inside Out”: curiosity stats, mood triggers, and celebrity alter-egos. 

As the saying goes -- “*Only the curious have something to find*” -- Destination Unknown will encourage you to embrace a bolder path.

Destination Unknown is designed and developed with love by **Shijie Feng**. You can connect with Shijie on [LinkedIn](https://www.linkedin.com/in/shijiefeng), [Twitter](https://twitter.com/Neon_Badger), and [Medium](https://medium.com/@ShijieF).


# Table of Contents
* [Technologies](#technologies)
* [Features](#features)
* [Set Up](#setup)
* [Testing](#testing)
* [Deployment](#deployment)
* [Future Features](#future)
* [Author](#author)
* [License](#license)
* [Acknowledgment](#acknowledgment)


## <a name="technologies"></a>Technologies

**Destination Unknown** is built on a Flask server (written in Python) and uses a PostgreSQL database. The application seamlessly integrates with Uber, Yelp, Mapbox, and Twilio APIs and adopts a modernized UI that supports full-screen video background, natural language form, and fun JavaScript/jQuery/CSS animation effects. While using Destination Unknown, users generate live data written into the database, and the application queries the database and visualizes the information with jQuery and D3.js.

## <a name="features"></a>Features

####Full-Screen Video Background

The landing page embeds HTML5 video in the background to create a stunning user experience. The video background is supported in all modern browsers (>IE8). For browsers incompatible with HTML5 video, a static full-screen picture is shown instead.

I create and my own video for the background. To make the video background work on the web, you have to host three formats:
* MP4 – a container for H.264 video and AAC audio
* Ogg – a container for Theora video and Vorbis audio
* WebM – a container intended primarily for use in the HTML5 video tag

####Login with Uber

User login is handled through Uber's OAuth 2.0, following the client-side web application flow. 

For a user to access Destination Unknown's content and request in-app Uber services, the application needs to get authorization from Uber, the resource owner, and will redirect the user to Uber's Authorization server, where he or she is asked to authenticate (if he or she is not already logged in) and then authorize the requested permissions. After successfully being granted access, the application is redirected to the redirect_uri address, including an access_token that can be used directly by the application to request information or perform operations on behalf of the user, including requesting a ride by Uber. Access_token is then encrypted and stored on the Flask session, and subsequent login will not prompt for the authorization dialog if the user is logged in and has previously approved the same permissions. For more, please see [Uber documentation](https://developer.uber.com/docs/authentication). 

####Mischievous User Avatar

After the user successfully logs in through Uber, the application accesses the user's Uber profile and displays it over the form. With a mouseover hover, you can turn into a curious cat!

####Natural Language User Interface

When I signed up for Beats Music (now Apple Music), it asked me to select music genres by completing a sentence ("I'M ____ & FEEL LIKE ____ WITH ____ TO ____"), which I found fun. 

With Destination Unknown, I experimented with this novel UI concept and implemented a Natural Language Form ("NLF"), embedding input fields inside sentences to make filling out a form as engaging as writing a mini story. In addition to asking for the user's current location, desired event type, and preferred destination for business discovery, the form collects the user's feelings at the time of search by asking about mood, self-description, and celebrity alter-ego for data visualization purposes. For more design inspirations on NLF, please visit this [blog post](http://www.jroehm.com/2014/01/ui-pattern-natural-language-form/). 

####Business Discovery

Destination Unknown uses the Yelp API behind the scene to determine the list of businesses to choose from. Once the user fills out the form and clicks the "Find Destination" button, the application sends the search parameters to Yelp's search endpoint. After Yelp returns business objects in JSON, the application randomly selects one of the highest-rated businesses for the user's consideration, revealing only the business's Yelp ratings, review snippet, and business categories -- just enough information to get you curious and excited!

####Story Book Map

The background map is built with the Mapbox API, rendered with a customized [picture book atlas theme](https://github.com/mapbox/mapbox-studio-picture-book.tm2) designed in Mapbox Studio. The map shows two custom-made markers: one for the user with a popup window greeting the user and indicating the user's current location, and the other for the mystery destination. The user has the option of returning to the previous search page, or requesting Uber to Destination Unknown.

####Uber Ride Request (sandbox)

A user can click "Call Uber" button and after confirming the ride request, the application sends an AJAX request to the Flask controller, sending along the geolocations of the user and the selected business. The application then uses the OAuth 2.0 credentials to instantiate a client object, makes a request to Uber's v1/requests endpoint that returns Uber products in the vincinity of the user, and picks a UberX (or UberXL if no UberX is available). The application then makes a sandbox ride request, changing product status to "accepted." After the ride request is successful, Uber returns a successful 200 status code, and the application can access the ride details including the driver's name and rating, the vehicle's make and model, and the estimated pickup. For more, please visit [Uber Rides API tutorial](https://developer.uber.com/docs/tutorials-rides-api).

####Twilio Text Message Confirmation

When the user's ride request is successful, the application uses the Twilio SMS API to send the ride information to the user.

####Live User-Generated Data

As the user fills out the form, all the form fields -- including the user's mood, trip description, and alter-ego -- are written into the database, along with the destination generated by the application. When the user requests Uber, the uber_request field is accordingly updated in the database.

####Curiosity and Mood Stats Visualization

The application makes SQLAlchemy queries into the database and returns the following data: the number of times the user has been curious and searched for a destination, the number of times the user has been bold and requested uber, and how many miles the user has traveled to Destination Unknown with Uber (in sandbox, at the moment). With jQuery, these stats are shown with a flipping countup animation effect. The user can also see the percentage of times he or she picked the celebrity alter-egos on a D3.js donut chart, and how the user's mood affects the activity choice on a D3.js chord diagram.


## <a name="testing"></a>Testing

The application has been tested with Unittest, integration test, and selenium. 


## <a name="setup"></a>Set Up

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

####Prerequisities

What things you need to install the software and how to install them

```
Give examples
```

####Installing

A step by step series of examples that tell you have to get a development env running

Stay what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

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


## <a name="author"></a>Author

* **Shijie Feng** - Github: [neonbadger](https://github.com/neonbadger)

## <a name="license"></a>License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## <a name="acknowledgments"></a>Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

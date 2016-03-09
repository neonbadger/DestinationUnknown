"""Models and database functions for Destination Unknown"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User logged in through Uber."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    img_url = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    phone = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_first_name=%s email=%s>" % (self.first_name, self.email)


class Search(db.Model):
    """Search history of the user."""

    __tablename__ = "searches"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    mood = db.Column(db.String(50))
    adjective = db.Column(db.String(50))
    alter_ego = db.Column(db.String(50))
    event = db.Column(db.String(50))
    location = db.Column(db.String(200))
    start_lat = db.Column(db.Float)
    start_lng = db.Column(db.Float)
    destination = db.Column(db.String(200))
    end_lat = db.Column(db.Float)
    end_lng = db.Column(db.Float)
    mileage = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    uber_request = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Search mood=%s event=%s destination=%s uber_requested=%s>" % ( 
            self.mood, self.event, self.destination, self.uber_request)


class Rating(db.Model):
    """User's post-trip rating and review."""

    __tablename__ = "ratings"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey("searches.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_rating = db.Column(db.Integer, nullable=True)
    user_comment = db.Column(db.Text, nullable=True)

    user = db.relationship('User',
                            backref=db.backref('ratings'))

    search = db.relationship('Search',
                            backref=db.backref('ratings'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating user_id=%d user_rating=%d>" % (self.user_id, self.user_rating)



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///trips'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

    db.create_all()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

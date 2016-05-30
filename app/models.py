from datetime import datetime
from app import db

# Create our database model


class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    id_incr = db.Column(db.Integer, db.Sequence('seq_user_id', start=1, increment=1))
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                        onupdate=datetime.utcnow)
    access_token = db.Column(db.String, nullable=False)

    def __init__(self, id, name, access_token):
        self.id = id
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.name = name
        self.access_token = access_token

    def __repr__(self):
        user_details = ""
        user_details += "<User %r>" % self.id

        return user_details

    def get_id_incr(self):
        return self.id_incr


class Movie(db.Model):
    __tablename__ = "Movies"

    id = db.Column(db.Integer, db.Sequence('seq_movie_id', start=1, increment=1), primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def get_movie_name(self):
        return self.name

    def get_movie_year(self):
        return self.year



from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_jsglue import JSGlue

webpack = Webpack()

app = Flask(__name__)
app.config.from_object('config')

webpack.init_app(app)
jsglue = JSGlue(app)

db = SQLAlchemy(app)

from models import User, Movie

with app.app_context():
    db.create_all()


""" example
user = User(id="awdad", name="nicename",
            profile_url="...",
            access_token="...")
db.session.add(user)
db.session.commit()

g.user = session.get('user', None)
print g.user
"""

"""
users = User.query.all()
print users
"""

FB_APP_ID = ""
FB_APP_NAME = ""
FB_APP_SECRET = ""

from app import views, models


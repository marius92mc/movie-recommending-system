from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_webpack import Webpack


webpack = Webpack()

app = Flask(__name__)
app.config.from_object('config')

webpack.init_app(app)

db = SQLAlchemy(app)

from models import User

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

FB_APP_ID = "361217287335942"
FB_APP_NAME = "MovieRecommendation"
FB_APP_SECRET = "3d0c5dc352649c11d5792d7f8f5a2e94"

from app import views, models


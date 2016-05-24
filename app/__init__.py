from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
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

from app import views, models
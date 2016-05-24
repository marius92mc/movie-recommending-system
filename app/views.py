import json
from engine import RecommendationEngine
import logging
from app import app, db

from flask import Flask, request
from flask import g, session

from models import User
from datetime import datetime

# main = Blueprint('main', __name__, static_folder="static", template_folder="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings_data = recommendation_engine.get_top_ratings(user_id, count)
    # -------------- db operations example ---------
    user = User(id="id0",
                created=datetime.utcnow(), updated=datetime.utcnow(),
                name="nicename",
                profile_url="...",
                access_token="...")
    if User.query.filter_by(id="id0").count() < 1:
        db.session.add(user)
        db.session.commit()

    users = User.query.all()
    print users
    # -----------------------------------------------
    return json.dumps(top_ratings_data)


@app.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])

    return json.dumps(ratings)


@app.route("/<int:user_id>/ratings", methods=["POST"])
def add_ratings(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the engine (user_id, movie_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)

    return json.dumps(ratings)


def create_recommendation_engine(spark_context, dataset_path, model_path):
    global recommendation_engine

    recommendation_engine = RecommendationEngine(spark_context,
                                                 dataset_path,
                                                 model_path)


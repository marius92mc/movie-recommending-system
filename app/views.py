from datetime import datetime
from time import time
import json
from engine import RecommendationEngine
import logging
from app import app, db

from app import FB_APP_ID, FB_APP_NAME, FB_APP_SECRET
from facebook import get_user_from_cookie, GraphAPI

from flask import g, render_template, Response, redirect, request, session, url_for
from models import User, Movie

from utils.util_funcs import UsersIndices
from utils.util_funcs import populate_movies_table

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dataset_id_from_db_id(db_id):
    """ Compute the int index of the user associated with the
        string facebook id from the model

    Params:
        db_id   - facebook user id

    Returns:
        user_id - associated id from the trained model
    """
    """ Example of type, components and calling
        a method for returning a specific column
        via method implemented in model's class

    for user in User.query.filter_by(id=user_id):
        print type(user)
        print user.__dict__
        print user.get_id_incr() // method implemented in models.py
    """
    user_in_db = False
    if User.query.filter_by(id=db_id).count() > 0:
        user_in_db = True
    if user_in_db is False:
        return -1

    index_db = int(User.query.filter_by(id=db_id).first().get_id_incr())
    temp_obj = UsersIndices()
    user_id = int(temp_obj.get_user_index_dataset(index_db))

    return user_id


@app.route("/")
def index():
    return render_template("client/index.html")


@app.route("/save_user", methods=["POST"])
def save_user():
    user = User(id=request.json['id'],
                name=request.json['name'],
                access_token=request.json['accessToken'])
    if User.query.filter_by(id=request.json['id']).count() < 1:
        db.session.add(user)
        db.session.commit()

    print User.query.all()

    return "user saved"


@app.route("/get_movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    movie_entries = []
    movies_until_now = {}

    for movie in movies:
        movie_entry = {}
        movie_entry['name'] = movie.get_movie_name()
        movie_entry['id_dataset'] = movie.get_id_dataset()
        if movie_entry['name'] not in movies_until_now:
            movie_entries.append(movie_entry)
        movies_until_now[movie_entry['name']] = True

    return json.dumps(movie_entries)


@app.route("/<string:user_id>/rating", methods=["POST"])
def add_rating(user_id):
    user_id = get_dataset_id_from_db_id(user_id)
    if user_id == -1:
        return json.dumps([])

    print request.json['movieName'], request.json['rating']
    query_result = Movie.query.filter_by(name=request.json['movieName'])
    if query_result.count() < 1:
        logger.info("Error, not a valid movie name")
        return json.dumps([])

    id_dataset = int(query_result.first().get_id_dataset())
    print user_id, id_dataset

    user_movie_rating = [[user_id, id_dataset, float(request.json['rating'])]]

    time0 = time()
    recommendation_engine.add_ratings(user_movie_rating)
    retrained_time = round(time() - time0, 3)

    return json.dumps(retrained_time)


@app.route("/<string:user_id>/bestratings/<int:num_movies>", methods=["GET"])
def get_best_ratings(user_id, num_movies):
    user_id = get_dataset_id_from_db_id(user_id)
    if user_id == -1:
        return json.dumps([])

    top_ratings_data = recommendation_engine.get_top_ratings(user_id, num_movies)

    return json.dumps(top_ratings_data)


@app.route("/<string:user_id>/predicted_rating", methods=["POST"])
def get_predicted_movie_rating(user_id):
    user_id = get_dataset_id_from_db_id(user_id)
    if user_id == -1:
        return json.dumps([])

    query_result = Movie.query.filter_by(name=request.json['movieName'])
    if query_result.count() < 1:
        logger.info("Error, not a valid movie name")
        return json.dumps([])

    id_movie_dataset = int(query_result.first().get_id_dataset())
    # print user_id, id_movie_dataset

    logger.debug("User %s rating requested for movie %s", user_id, id_movie_dataset)
    movie_rating = recommendation_engine.get_ratings_for_movie_ids(user_id, [id_movie_dataset])

    if len(movie_rating[0]) < 3:
        return json.dumps([])
    predicted_movie = {}
    predicted_movie['movieName'] = request.json['movieName']
    predicted_movie['rating'] = round(movie_rating[0][1], 3)
    if predicted_movie['rating'] < 1:
        predicted_movie['rating'] = 1

    return json.dumps(predicted_movie)




@app.route("/<string:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    user_id = get_dataset_id_from_db_id(user_id)
    if user_id == -1:
        return json.dumps([])

    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings_data = recommendation_engine.get_top_ratings(user_id, count)
    # -------------- db operations example ---------
    """
    user = User(id="id0",
                name="nicename",
                access_token="...")
    if User.query.filter_by(id="id0").count() < 1:
        db.session.add(user)
        db.session.commit()

    users = User.query.all()
    print users
    """
    # -----------------------------------------------
    return json.dumps(top_ratings_data)


@app.route("/<string:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    user_id = get_dataset_id_from_db_id(user_id)
    if user_id == -1:
        return json.dumps([])

    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])

    return json.dumps(ratings)


@app.route("/<string:user_id>/ratings", methods=["POST"])
def add_ratings(user_id):
    user_id = get_dataset_id_from_db_id(user_id)
    if user_id == -1:
        return json.dumps([])

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

    populate_movies_table(spark_context, dataset_path)

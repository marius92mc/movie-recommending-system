from datetime import datetime
import time
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





# -------------------------------------------------- to delete
# @app.route("/")
def index():
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    if g.user:
        return render_template('index.html', app_id=FB_APP_ID,
                               app_name=FB_APP_NAME, user=g.user)
    # Otherwise, a user is not logged in.

    return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME)


# @app.route('/logout')
def logout():
    """ Log out the user from the application.
    Log out the user from the application by removing them from the
    session.
    Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    session.pop('user', None)
    return redirect(url_for('index'))


# @app.before_request
def get_current_user():
    """Set g.user to the currently logged in user.
    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.  A currently logged in user is
    determined by seeing if it exists in Flask's session dictionary.
    If it is the first time the user is logging into this application it will
    create the user and insert it into the database.  If the user is not logged
    in, None will be set to g.user.
    """

    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    if session.get('user'):
        g.user = session.get('user')
        return

    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)

    # If there is no result, we assume the user is not logged in.
    if result:
        # Check to see if this user is already in our database.
        user = User.query.filter(User.id == result['uid']).first()

        if not user:
            # Not an existing user so get info
            graph = GraphAPI(result['access_token'])
            profile = graph.get_object('me')
            if 'link' not in profile:
                profile['link'] = ""

            # Create the user and insert it into the database
            user = User(id=str(profile['id']), name=profile['name'],
                        profile_url=profile['link'],
                        access_token=result['access_token'])
            db.session.add(user)
        elif user.access_token != result['access_token']:
            # If an existing user, update the access token
            user.access_token = result['access_token']

        # Add the user to the current session
        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token)

    # Commit changes to the database and set the user as a global g.user
    db.session.commit()
    g.user = session.get('user', None)

# --------------------------------------------------


@app.route('/api/comments', methods=['GET', 'POST'])
def comments_handler():
    with open('comments.json', 'r') as f:
        comments = json.loads(f.read())

    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment['id'] = int(time.time() * 1000)
        comments.append(new_comment)

        with open('comments.json', 'w') as f:
            f.write(json.dumps(comments, indent=4, separators=(',', ': ')))

    return Response(
        json.dumps(comments),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

# ----------------------------------------------------- /to delete


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

    for movie in movies:
        movie_entry = {}
        movie_entry['name'] = movie.get_movie_name()
        movie_entry['id_dataset'] = movie.get_id_dataset()
        movie_entries.append(movie_entry)

    return json.dumps(movie_entries)


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

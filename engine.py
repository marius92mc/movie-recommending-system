import os
import shutil
from time import time
from pyspark.mllib.recommendation import ALS
from pyspark.mllib.recommendation import MatrixFactorizationModel

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_counts_and_averages(id_and_ratings_tuple):
    """ Computes counts and averages for movies

    Params:
        ID_and_ratings_tuple - a tuple (movie_id, ratings_iterable)

    Returns:
        (movie_id, (ratings_count, ratings_avg))
    """
    nratings = len(id_and_ratings_tuple[1])
    return id_and_ratings_tuple[0], \
           (nratings, float(sum(x for x in id_and_ratings_tuple[1])) / nratings)


class RecommendationEngine:
    """ A movie recommendation engine
    """

    def __init__(self, spark_context, dataset_path, model_path):
        """Init the recommendation engine given a Spark context and a dataset path
        """
        logger.info("Starting up the Recommendation Engine... ")
        self.sc = spark_context

        # Load ratings data for later use
        logger.info("Loading Ratings data...")
        ratings_file_path = os.path.join(dataset_path, 'ratings.csv')
        ratings_raw_rdd = self.sc.textFile(ratings_file_path)
        ratings_raw_data_header = ratings_raw_rdd.take(1)[0]

        self.ratings_rdd = ratings_raw_rdd.filter(lambda line: line != ratings_raw_data_header)\
            .map(lambda line: line.split(","))\
            .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))).cache()

        # Load movies data for later use
        logger.info("Loading Movies data...")
        movies_file_path = os.path.join(dataset_path, 'movies.csv')
        movies_raw_rdd = self.sc.textFile(movies_file_path)
        movies_raw_data_header = movies_raw_rdd.take(1)[0]

        self.movies_rdd = movies_raw_rdd.filter(lambda line: line != movies_raw_data_header)\
            .map(lambda line: line.split(","))\
            .map(lambda tokens: (int(tokens[0]), tokens[1].replace('"', ''), tokens[2])).cache()

        self.movies_titles_rdd = self.movies_rdd.map(lambda x: (int(x[0]), x[1])).cache()

        # Pre-calculate movies ratings counts
        self.__count_and_average_ratings()

        # Path of the saved model
        self.model_path = model_path

        self.model = ""

        # Train the model
        self.rank = 8
        self.seed = 5L
        self.iterations = 10
        self.regularization_parameter = 0.1
        if self.load_model() is False:
            self.__train_model()
            self.save_model()

    def __count_and_average_ratings(self):
        """ Updates the movies ratings counts
        from the current data self.ratings_rdd
        """
        logger.info("Counting movie ratings...")
        movie_id_with_ratings_rdd = self.ratings_rdd.map(lambda x: (x[1], x[2])).groupByKey()
        movie_id_with_avg_ratings_rdd = movie_id_with_ratings_rdd.map(get_counts_and_averages)
        self.movies_rating_counts_rdd = movie_id_with_avg_ratings_rdd.map(lambda x: (x[0], x[1][0]))

    def save_model(self):
        if self.model != "":
            if os.path.isdir(self.model_path):
                shutil.rmtree(self.model_path)
            self.model.save(self.sc, self.model_path)
            logger.info("ALS model saved")

    def load_model(self):
        if os.path.isdir(self.model_path):
            self.model = MatrixFactorizationModel.load(self.sc, self.model_path)
            logger.info("ALS model loaded")
            return True
        return False

    def __train_model(self):
        """ Train the ALS model with the current dataset
        """
        logger.info("Training the ALS model...")
        t0 = time()
        self.model = ALS.train(self.ratings_rdd, self.rank, seed=self.seed,
                               iterations=self.iterations, lambda_=self.regularization_parameter)
        train_time = time() - t0
        print "New model trained in %s seconds" % round(train_time,3)
        logger.info("ALS model built")

    def __predict_ratings(self, user_and_movie_rdd):
        """ Gets predictions for a given user (user_id, movie_id) formatted rdd

        Params:
            (user_id, movie_id) formatted rdd

        Returns:
            an rdd with format (movie_title, movie_rating, num_ratings)
        """
        predicted_rdd = self.model.predictAll(user_and_movie_rdd)
        predicted_rating_rdd = predicted_rdd.map(lambda x: (x.product, x.rating))

        predicted_rating_title_and_count_rdd = \
            predicted_rating_rdd.join(self.movies_titles_rdd).join(self.movies_rating_counts_rdd)
        predicted_rating_title_and_count_rdd = \
            predicted_rating_title_and_count_rdd.map(lambda r: (r[1][0][1], r[1][0][0], r[1][1]))

        predicted_rating_title_and_count_rdd = \
            predicted_rating_title_and_count_rdd.filter(lambda r: (r[1] >= 1 and r[1] <= 5))
        
        return predicted_rating_title_and_count_rdd

    def add_ratings(self, ratings):
        """ Add additional movie ratings to the model in the format
        (user_id, movie_id, rating)

        Params:
            ratings - (user_id, movie_id, rating)
        """
        # Convert ratings to an rdd
        new_ratings_rdd = self.sc.parallelize(ratings)
        # Add new ratings to the existing ones in the model
        self.ratings_rdd = self.ratings_rdd.union(new_ratings_rdd)
        # Re-compute movie ratings count
        self.__count_and_average_ratings()
        # Re-train the ALS model with the new ratings
        """ TODO make it kindof asynchron, because the training will take
        long time.
        Or make it to call the train method only after a number of x
        users already made this requests
        """
        self.__train_model()
        self.save_model()

        return ratings

    def get_ratings_for_movie_ids(self, user_id, movie_ids):
        """ Predict ratings for user with user_id for movies with movie_ids

        Params:
            user_id   - id of a specific user
            movie_ids - list of ids of movies

        Returns:
            ratings - (user_id, movie_id, rating)
        """
        requested_movies_rdd = self.sc.parallelize(movie_ids).map(lambda x: (user_id, x))
        # Get predicted ratings
        ratings = self.__predict_ratings(requested_movies_rdd).collect()

        return ratings

    def get_top_ratings(self, user_id, movies_count):
        """ Recommends up to movies_count top unrated movies to user_id

        Params:
            user_id   - id of a specific user
            movie_count - number of movies to retrive

        Returns:
            ratings
        """
        # Get pairs of (userID, movieID) for user_id unrated movies
        user_unrated_movies_rdd = self.movies_rdd.filter(lambda rating: not rating[1] == user_id)\
                                                  .map(lambda x: (user_id, x[0]))
        # Get predicted ratings
        ratings = self.__predict_ratings(user_unrated_movies_rdd).filter(lambda r: r[2] >= 25)\
                                                                 .takeOrdered(movies_count,
                                                                              key=lambda x: -x[1])

        return ratings


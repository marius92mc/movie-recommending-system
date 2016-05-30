import os
import re
from app import db
from app.models import Movie
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UsersIndices:
    def __init__(self):
        self.starting_index = 300000

    def get_user_index_dataset(self, index_db):
        return self.starting_index + index_db


def get_movies_name(spark_context, dataset_path):
    movies_file_path = os.path.join(dataset_path, 'movies.csv')
    movies_raw_rdd = spark_context.textFile(movies_file_path)
    movies_raw_data_header = movies_raw_rdd.take(1)[0]

    movies_rdd = movies_raw_rdd.filter(lambda line: line != movies_raw_data_header)\
        .map(lambda line: line.split(","))\
        .map(lambda tokens: (int(tokens[0]), tokens[1], tokens[2])).cache()

    movies_name_rdd = movies_rdd.map(lambda x: (x[1]))

    return movies_name_rdd.collect()


def populate_movies_table(spark_context, dataset_path):
    if len(Movie.query.all()) > 0:
        return False

    movies_name = get_movies_name(spark_context, dataset_path)

    count_movies_db = 0
    for movie_name in movies_name:
        p = re.compile(r'\([^)]*\)')
        name = re.sub(p, '', movie_name)
        years = re.findall('\((.*?)\)', movie_name)

        year = -1
        for year_entry in years:
            if year_entry.isdigit():
                year = int(year_entry)
                break

        if year > 2008:
            movie = Movie(name=name,
                          year=year)
            db.session.add(movie)
            db.session.commit()
            count_movies_db += 1


    logger.info("Filled " +
                str(count_movies_db) +
                " movie entries in database...")

    return True

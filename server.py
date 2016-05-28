import cherrypy
import os
import sys
from paste.translogger import TransLogger
# from app import create_app
from pyspark import SparkContext, SparkConf

from app import app
from app.views import create_recommendation_engine


def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("movie_recommendation-server")
    """               .setMaster(...)
                      .set("spark.executor.memory", "2g")
                      .set("spark.cores.max", "10")
    Properties set directly on the SparkConf take highest precedence,
    then flags passed to spark-submit or spark-shell,
    then options in the spark-defaults.conf file.
    """
    # IMPORTANT: pass additional Python modules to each worker
    spark_context = SparkContext(conf=conf, pyFiles=['app/__init__.py',
                                                     'engine.py',
                                                     'app/views.py',
                                                     'app/models.py'])

    return spark_context


def run_server(app):
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5435,  # initially was 5432
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


def main(argv):
    ml_latest = "ml-latest"
    ml_latest_small = "ml-latest-small"
    dataset = ml_latest

    if len(argv) > 1:
        if argv[0] == "--dataset":
            if argv[1] == ml_latest or argv[1] == ml_latest_small:
                dataset = argv[1]
    print "Using ", dataset, " dataset..."

    # Init spark context and load libraries
    sc = init_spark_context()
    dataset_path = os.path.join("datasets", dataset)
    model_path = os.path.join("saved_models", "movie_lens_als")

    create_recommendation_engine(sc, dataset_path, model_path)
    """
    from app import global_config
    if global_config['app'] is "":
        print "NOK"
    else:
        print "OK"
    """

    # start web server
    run_server(app)


if __name__ == "__main__":
    main(sys.argv[1:])


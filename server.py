import cherrypy
import os
from paste.translogger import TransLogger
from app import create_app
from pyspark import SparkContext, SparkConf


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
    spark_context = SparkContext(conf=conf, pyFiles=['engine.py', 'app.py'])

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
        'server.socket_port': 5433,  # initially was 5432
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    # Init spark context and load libraries
    sc = init_spark_context()
    dataset_path = os.path.join('datasets', 'ml-latest')
    app = create_app(sc, dataset_path)

    # start web server
    run_server(app)


from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = True
SECRET_KEY = 'keep_it_like_a_secret'

# Database details
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/rs'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Webpack assets
WEBPACK_MANIFEST_PATH = BASE_DIRECTORY + '/build/manifest.json'


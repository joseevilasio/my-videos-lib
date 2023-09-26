import os

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def configure(app: Flask):
    mongo_uri = os.getenv("MONGODB_URI")

    if os.getenv("FLASK_ENV") == "production":
        mongo.init_app(app, uri=mongo_uri)

    else:
        mongo.init_app(app)

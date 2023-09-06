from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def configure(app: Flask):
    mongo.init_app(app)

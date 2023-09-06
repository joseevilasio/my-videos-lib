from dynaconf import settings
from flask import Flask

from api.config import configure


def return_a_value():
    return settings.VALUE


def create_app():
    app = Flask(__name__)
    configure(app)
    return app

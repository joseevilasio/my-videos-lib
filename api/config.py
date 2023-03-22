import os
from dynaconf import FlaskDynaconf
from flask import Flask

HERE = os.path.dirname(os.path.abspath(__file__))


def configure(app: Flask):
    FlaskDynaconf(app, extensions_list="EXTENSIONS", root_path=HERE)

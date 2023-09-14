import os

from dynaconf import Dynaconf, FlaskDynaconf
from flask import Flask

HERE = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    settings_files=["settings.toml", ".secrets.toml"],
)


def configure(app: Flask):
    FlaskDynaconf(app, extensions_list="EXTENSIONS", root_path=HERE)

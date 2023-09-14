import json
import re

from flask import Flask
from flask_jwt_extended import JWTManager

from api.database import mongo

jwt = JWTManager()


def get_next_sequence_value(db_name: str):
    """Create unique id in each collection"""
    sequence = mongo.db.sequences.find_one_and_update(
        {"_id": db_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True,
    )
    return sequence["sequence_value"]


def is_valid_url(url: str):
    """Regular expression to check basic URL format"""
    url_pattern = re.compile(
        r"^(https?://)?"  # Protocolo (opcional)
        r"([A-Za-z_0-9.-]+)"  # Nome de host (obrigatório)
        r"(:\d+)?"  # Porta (opcional)
        r"(/[^?#]*)?"  # Caminho (opcional)
        r"(\?[^#]*)?"  # Query string (opcional)
        r"(#.*)?$"  # Fragmento (opcional)
    )

    # Verificar se a URL corresponde ao padrão
    return bool(url_pattern.match(url))


def returns_if_category_exists(title: str):
    """Check if category already exists"""
    # TODO: Utilizar REGEX para buscar tanto em uppercase como em lowercase
    query = mongo.db.category.find_one(
        {"title": f"{title}"}, projection={"_id": False}
    )
    if query is not None:
        return True
    return False


def convert_json_for_dict(data) -> dict:
    with open(data, "r") as data_json:
        data = json.load(data_json)

    return data


def configure(app: Flask):
    jwt.init_app(app)

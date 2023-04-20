from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlmodel import Session, create_engine

from api import model

db = SQLAlchemy()

# db.create_all()
SQLALCHEMY_DATABASE_URI = "sqlite:///assets/database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
model.SQLModel.metadata.create_all(bind=engine)


def get_session() -> Session:
    return Session(engine)


def configure(app: Flask):
    db.init_app(app)

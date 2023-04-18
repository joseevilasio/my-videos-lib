from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlmodel import Session, SQLModel, create_engine

db = SQLAlchemy()

# db.create_all()
SQLALCHEMY_DATABASE_URI = "sqlite:///api/database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
SQLModel.metadata.create_all(bind=engine)


def get_session() -> Session:
    return Session(engine)


def configure(app: Flask):
    db.init_app(app)

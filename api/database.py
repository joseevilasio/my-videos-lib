from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine("sqlite:///api/database.db")
# metadata = MetaData(bind=engine)
conn = engine.connect()

db = SQLAlchemy()


def configure(app: Flask):
    db.init_app(app)


conn.exec_driver_sql(
    """\
    CREATE TABLE if not exists video (
        id integer PRIMARY KEY AUTOINCREMENT,
        title varchar UNIQUE NOT NULL,
        description varchar NOT NULL,
        url varchar NOT NULL
    );
    """
)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = "sqlite:///api/database.db"

db = SQLAlchemy()

engine = create_engine(SQLALCHEMY_DATABASE_URI)
conn = engine.connect()


def configure(app: Flask):
    db.init_app(app)


create_table_sql = """\
    CREATE TABLE if not exists video (
        id integer PRIMARY KEY AUTOINCREMENT,
        title varchar UNIQUE NOT NULL,
        description varchar NOT NULL,
        url varchar NOT NULL
    );
    """

conn.exec_driver_sql(create_table_sql)

from sqlite3 import connect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData


engine = create_engine("sqlite:///api/database.db")
#metadata = MetaData(bind=engine)
conn = engine.connect()

db = SQLAlchemy()

def configure(app):
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

videos = [
    {
        "title": "Engenheiro de software ou Programador? com Paulo Silveira",
        "description": "Engenheiro de software, pessoa que programa ou dev, o que você é? ",
        "url": "https://www.youtube.com/watch?v=Gm6U-AxXEQ0",
    },
    {
        "title": "Estrutura de dados com Roberta Arcoverde",
        "description": "O que são estrutura de dados e como podem ser aplicadas na programação?",
        "url": "https://www.youtube.com/watch?v=57VqgNjbzrg",
    },
]

count = conn.exec_driver_sql("SELECT * FROM video;").fetchall()
if not count:
    conn.exec_driver_sql(
        """\
        INSERT INTO video(title, description, url)
        VALUES (:title, :description, :url);
        """,
        videos,
    )
    
videos = conn.exec_driver_sql("SELECT * FROM video;").fetchall()
assert len(videos) >= 2

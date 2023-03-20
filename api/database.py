from sqlite3 import connect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure(app):
    db.init_app(app)

conn = connect("database.db")
cursor = conn.cursor()

conn.execute(
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

count = cursor.execute("SELECT * FROM video;").fetchall()
if not count:
    cursor.executemany(
        """\
        INSERT INTO video(title, description, url)
        VALUES (:title, :description, :url);
        """,
        videos,
    )
    conn.commit()

videos = cursor.execute("SELECT * FROM video;").fetchall()
assert len(videos) >= 2

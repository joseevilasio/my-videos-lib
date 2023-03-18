from sqlite3 import connect

conn = connect("database.db")
cursor = conn.cursor()

conn.execute(
    """\
    CREATE TABLE if not exists post (
        id integer PRIMARY KEY AUTOINCREMENT,
        title varchar UNIQUE NOT NULL,
        description varchar NOT NULL,
        url varchar NOT NULL
    );
    """
)

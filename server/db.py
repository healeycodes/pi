import os

TEST_DB = os.environ["TEST_DB"] if "TEST_DB" in os.environ else None
DATABASE_URL = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else None
FORMAT_STRING = (
    "%s" if DATABASE_URL else "?"
)  # (sqlite uses `?` but postgresql uses `%s`)


class _DB:
    """
    An instance of a database. Connected to either sqlite or postgresql.
    Should be retrieved from `db.get_db` rather than called directly.
    """

    def __init__(self, mode="sqlite", addr="", uri=False):
        self.connection = None
        self.mode = mode
        self.addr = addr
        self.uri = uri
        self.connect()

    def connect(self):
        if self.mode != "sqlite":
            import psycopg2

            self.connection = psycopg2.connect(self.addr, sslmode="require")
        else:
            import sqlite3

            self.connection = sqlite3.connect(self.addr, uri=self.uri)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def setup(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS message_queue (
                id INTEGER PRIMARY KEY,
                status varchar(256) NOT NULL,
                text varchar(256) NOT NULL,
                name varchar(256) NOT NULL,
                timestamp varchar(256) NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS satellites (
                id INTEGER PRIMARY KEY,
                prn varchar(128),
                status INTEGER,
                description varchar(2048),
                timestamp varchar(256) NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY,
                temperature varchar(128),
                humidity varchar(128),
                timestamp varchar(256) NOT NULL
            )
            """
        )
        self.connection.commit()


def get_db():
    """
    Get the relevant database connection.
        - PostgreSQL when we're in production on heroku
        - Memory database for testing
        - Shared memory file database for dev
    """
    if TEST_DB:
        database = _DB(mode="sqlite", addr=TEST_DB, uri=True)
    elif DATABASE_URL:
        database = _DB(mode="postgresql", addr=DATABASE_URL, uri=False)
    else:
        database = _DB(mode="sqlite", addr="dev.db", uri=True)

    # create tables if required
    database.setup()
    return database

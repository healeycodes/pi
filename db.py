import os

"""
We use sqlite3 locally but PostgreSQL on the Heroku Dyno.
"""

DATABASE_URL = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else None

# handle the different formatting string (sqlite uses `?` but postgresql uses `%s`)
FORMAT_STRING = "%s" if DATABASE_URL else "?"


def connect():
    if DATABASE_URL:
        import psycopg2

        connection = psycopg2.connect(DATABASE_URL, sslmode="require")
    else:
        import sqlite3

        connection = sqlite3.connect("file::memory:?cache=shared", uri=True)
    cursor = connection.cursor()
    return connection, cursor


def close(connection):
    connection.commit()
    connection.close()


def setup():
    connection, cursor = connect()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS message_queue (
            id serial PRIMARY KEY,
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
            id serial PRIMARY KEY,
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
            id serial PRIMARY KEY,
            temperature varchar(128),
            humidity varchar(128),
            timestamp varchar(256) NOT NULL
        )
        """
    )
    close(connection)


setup()

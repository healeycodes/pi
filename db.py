import os

"""
We use sqlite3 locally but postgresql on the dyno.
"""

DATABASE_URL = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else None


def connect():
    if DATABASE_URL:
        import psycopg2

        connection = psycopg2.connect(DATABASE_URL, sslmode="require")
    else:
        import sqlite3

        connection = sqlite3.connect("dev.db")
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
            name varchar(256) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS satellites (
            current varchar(2048)
        )
        """
    )
    close(connection)


setup()

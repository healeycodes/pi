import os

DATABASE_URL = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else None

if not DATABASE_URL:
    import psycopg2

    def connect():
        connection = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = connection.cursor()
        return connection, cursor


else:
    import sqlite3

    def connect():
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
    close(connection)


setup()

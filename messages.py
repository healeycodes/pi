import os
import psycopg2
from datetime import datetime
from dataclasses import dataclass

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_NAME = "messages"


@dataclass
class Message:
    msg_id: str
    status: str
    text: str
    user: str


def connect():
    connection = psycopg2.connect(DATABASE_URL, dbname=DATABASE_NAME, sslmode="require")
    cursor = connection.cursor()
    return connection, cursor


def update_msg_status(msg_id, status):
    connection, cursor = connect()
    cursor.execute("UPDATE queue set status=%s WHERE msg=%s", (status, msg_id))
    cursor.close()
    connection.close()


def get_msg():
    connection, cursor = connect()
    cursor.execute(
        "SELECT (id, status, text, user) WHERE status LIKE 'queued%' LIMIT 1"
    )
    row = cursor.fetchone()
    msg = Message(
        msg_id=row[0],
        status=row[1],
        text=row[2],
        user=row[3],
    )
    cursor.close()
    connection.close()
    return msg


def put_msg(msg, user):
    status = f"queued: {datetime.now()}"
    connection, cursor = connect()
    cursor.execute(
        "INSERT INTO queue (status, text, user) VALUES (%s, %s, %s) RETURNING id",
        (status, text, user),
    )
    msg_id = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return msg_id


def check_msg(msg_id):
    connection, cursor = connect()
    cursor.execute("SELECT (status) WHERE id=%s", (msg_id))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]


def setup():
    connection = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DATABASE_NAME}'"
    )
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS queue (
        id serial PRIMARY KEY,
        status varchar(256) NOT NULL,
        text varchar(256) NOT NULL,
        user varchar(256) NOT NULL,
        )
        """
    )

    connection.commit()
    cursor.close()
    connection.close()


setup()

import os
import psycopg2
from datetime import datetime
from dataclasses import dataclass

DATABASE_URL = os.environ["DATABASE_URL"]


@dataclass
class Message:
    msg_id: str
    status: str
    text: str
    name: str


def connect():
    connection = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = connection.cursor()
    return connection, cursor


def update_msg_status(msg_id, status):
    connection, cursor = connect()
    cursor.execute("UPDATE queue set status=%s WHERE id=%s", (status, msg_id))
    close(connection)


def get_msg():
    connection, cursor = connect()
    cursor.execute(
        "SELECT id, status, text, name FROM queue WHERE status LIKE 'queued%' LIMIT 1"
    )
    row = cursor.fetchone()
    msg = Message(
        msg_id=row[0],
        status=row[1],
        text=row[2],
        name=row[3],
    )
    close(connection)
    return msg


def put_msg(text, name):
    status = f"queued at {datetime.now()}"
    connection, cursor = connect()
    cursor.execute(
        "INSERT INTO queue (status, text, name) VALUES (%s, %s, %s) RETURNING id",
        (status, text, name),
    )
    msg_id = cursor.fetchone()[0]
    close(connection)
    return msg_id


def check_msg(msg_id):
    connection, cursor = connect()
    cursor.execute("SELECT status FROM queue WHERE id=%s", (msg_id))
    row = cursor.fetchone()
    close(connection)
    if row:
        return row[0]


def close(connection):
    connection.commit()
    connection.close()


def setup():
    connection, cursor = connect()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS queue (
        id serial PRIMARY KEY,
        status varchar(256) NOT NULL,
        text varchar(256) NOT NULL,
        name varchar(256) NOT NULL
        )
        """
    )
    close(connection)


setup()

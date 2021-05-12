import os
import psycopg2
from datetime import datetime
from dataclasses import dataclass

DATABASE_URL = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else None


@dataclass
class Message:
    msg_id: str
    status: str
    text: str
    name: str

    def debug(self):
        return f"{self.msg_id} | {self.status} | {self.text} | {self.name}"


def connect():
    connection = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = connection.cursor()
    return connection, cursor


def put_msg(text, name):
    status = f"queued at {datetime.now()}"
    connection, cursor = connect()
    cursor.execute(
        "INSERT INTO message_queue (status, text, name) VALUES (%s, %s, %s) RETURNING id",
        (status, text, name),
    )
    msg_id = cursor.fetchone()[0]
    close(connection)
    return msg_id


def update_msg_status(msg_id, status):
    connection, cursor = connect()
    cursor.execute("UPDATE message_queue set status=%s WHERE id=%s", (status, msg_id))
    close(connection)


def check_msg(msg_id):
    connection, cursor = connect()
    cursor.execute("SELECT status FROM message_queue WHERE id=%s", (msg_id,))
    row = cursor.fetchone()
    close(connection)
    if row:
        return row[0]


def get_msgs():
    connection, cursor = connect()
    cursor.execute(
        "SELECT id, status, text, name FROM message_queue WHERE status LIKE 'queued%' LIMIT 1"
    )
    row = cursor.fetchone()
    if row:
        return Message(msg_id=row[0], status=row[1], text=row[2], name=row[3],)
    close(connection)


def list_msgs():
    connection, cursor = connect()
    cursor.execute("SELECT id, status, text, name FROM message_queue")
    rows = cursor.fetchall()
    close(connection)
    return [
        Message(msg_id=row[0], status=row[1], text=row[2], name=row[3],) for row in rows
    ]


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


if DATABASE_URL:
    setup()

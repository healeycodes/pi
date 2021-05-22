from db import connect, close
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Message:
    msg_id: str
    status: str
    text: str
    name: str


def put_msg(text, name):
    status = f"queued at {datetime.now()}"
    connection, cursor = connect()
    cursor.execute(
        "INSERT INTO message_queue (status, text, name) VALUES (%s, %s, %s) RETURNING id",
        (status, text, name),
    )
    msg = Message(msg_id=cursor.fetchone()[0],)
    close(connection)
    return msg


def update_msg_status(msg_id, status):
    connection, cursor = connect()
    cursor.execute("UPDATE message_queue set status=%s WHERE id=%s", (status, msg_id))
    close(connection)


def check_msg(msg_id):
    connection, cursor = connect()
    cursor.execute(
        "SELECT id, status, text, name FROM message_queue WHERE id=%s", (msg_id,)
    )
    row = cursor.fetchone()
    close(connection)
    if row:
        return Message(msg_id=row[0], status=row[1], text=row[2], name=row[3],)


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

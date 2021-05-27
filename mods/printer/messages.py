from db import connect, close
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Message:
    msg_id: str
    status: str
    text: str
    name: str
    timestamp: str


def put_msg(text, name):
    status = f"queued at {datetime.now()}"
    connection, cursor = connect()
    cursor.execute(
        "INSERT INTO message_queue (status, text, name, timestamp) VALUES (%s, %s, %s, %s) RETURNING id",
        (status, text, name, datetime.now()),
    )
    msg_id = cursor.fetchone()[0]
    close(connection)
    return msg_id


def update_msg_status(msg_id, status):
    connection, cursor = connect()
    cursor.execute(
        "UPDATE message_queue set status=%s, timestamp=%s WHERE id=%s",
        (status, datetime.now(), msg_id),
    )
    close(connection)


def check_msg(msg_id):
    connection, cursor = connect()
    cursor.execute(
        "SELECT id, status, text, name, timestamp FROM message_queue WHERE id=%s",
        (msg_id,),
    )
    row = cursor.fetchone()
    close(connection)
    if row:
        return Message(
            msg_id=row[0], status=row[1], text=row[2], name=row[3], timestamp=row[4],
        )


def get_msgs():
    connection, cursor = connect()
    cursor.execute(
        "SELECT id, status, text, name, timestamp FROM message_queue WHERE status LIKE 'queued%' LIMIT 1"
    )
    row = cursor.fetchone()
    if row:
        return Message(
            msg_id=row[0], status=row[1], text=row[2], name=row[3], timestamp=row[4],
        )
    close(connection)


def list_msgs():
    connection, cursor = connect()
    cursor.execute("SELECT id, status, text, name, timestamp FROM message_queue")
    rows = cursor.fetchall()
    close(connection)
    return [
        Message(
            msg_id=row[0], status=row[1], text=row[2], name=row[3], timestamp=row[4],
        )
        for row in rows
    ]

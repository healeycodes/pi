import os
from datetime import datetime
from dataclasses import dataclass
from server.db import get_db, FORMAT_STRING as F


@dataclass
class Message:
    msg_id: str
    status: str
    text: str
    name: str
    timestamp: str


def put_msg(text, name):
    db = get_db()
    cursor = db.connection.cursor()
    status = f"queued at {datetime.now()}"

    # TODO: find a agnostic way of doing the following..
    # sqlite doesn't like 'RETURNING' (at least in the version that's bundled with python)
    # and postgresql doesn't like 'lastrowid'!
    if "DATABASE_URL" in os.environ:
        cursor.execute(
            f"INSERT INTO message_queue (status, text, name, timestamp) VALUES ({F}, {F}, {F}, {F}) RETURNING id",
            (status, text, name, datetime.now()),
        )
        msg_id = cursor.fetchone()[0]
    else:
        cursor.execute(
            f"INSERT INTO message_queue (status, text, name, timestamp) VALUES ({F}, {F}, {F}, {F})",
            (status, text, name, datetime.now()),
        )
        msg_id = cursor.lastrowid

    db.close()
    return msg_id


def update_msg_status(msg_id, status):
    db = get_db()
    cursor = db.connection.cursor()

    cursor.execute(
        f"UPDATE message_queue set status={F}, timestamp={F} WHERE id={F}",
        (status, datetime.now(), msg_id),
    )
    db.close()


def check_msg(msg_id):
    db = get_db()
    cursor = db.connection.cursor()

    cursor.execute(
        f"SELECT id, status, text, name, timestamp FROM message_queue WHERE id={F}",
        (msg_id,),
    )
    row = cursor.fetchone()
    db.close()
    if row:
        return Message(
            msg_id=row[0], status=row[1], text=row[2], name=row[3], timestamp=row[4],
        )


def get_msg():
    db = get_db()
    cursor = db.connection.cursor()

    cursor.execute(
        "SELECT id, status, text, name, timestamp FROM message_queue WHERE status LIKE 'queued%' ORDER BY id ASC LIMIT 1"
    )
    row = cursor.fetchone()
    db.close()
    if row:
        return Message(
            msg_id=row[0], status=row[1], text=row[2], name=row[3], timestamp=row[4],
        )


def list_msgs():
    db = get_db()
    cursor = db.connection.cursor()

    cursor.execute("SELECT id, status, text, name, timestamp FROM message_queue")
    rows = cursor.fetchall()
    db.close()

    return [
        Message(
            msg_id=row[0], status=row[1], text=row[2], name=row[3], timestamp=row[4],
        )
        for row in rows
    ]

from server.db import get_db, FORMAT_STRING as F
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Weather:
    temperature: float
    humidity: float
    timestamp: str


def save_weather(temperature, humidity):
    db = get_db()
    cursor = db.connection.cursor()

    # for now, don't keep weather logs
    cursor.execute("DELETE from weather")

    cursor.execute(
        f"INSERT INTO weather (temperature, humidity, timestamp) VALUES ({F}, {F}, {F})",
        (temperature, humidity, datetime.now(),),
    )
    db.close()


def get_weather():
    db = get_db()
    cursor = db.connection.cursor()

    cursor.execute(
        "SELECT temperature, humidity, timestamp FROM weather ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    if row:
        return Weather(
            temperature=float(row[0]), humidity=float(row[1]), timestamp=row[2],
        )
    db.close()

from db import connect, close, FORMAT_STRING as F
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Weather:
    temperature: float
    humidity: float
    timestamp: str


def save_weather(temperature, humidity):
    connection, cursor = connect()

    # for now, don't keep weather logs
    cursor.execute("DELETE from weather")

    cursor.execute(
        f"INSERT INTO weather (temperature, humidity, timestamp) VALUES ({F}, {F}, {F})",
        (temperature, humidity, datetime.now(),),
    )
    close(connection)


def get_weather():
    connection, cursor = connect()
    cursor.execute(
        "SELECT temperature, humidity, timestamp FROM weather ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    close(connection)
    if row:
        return Weather(
            temperature=float(row[0]), humidity=float(row[1]), timestamp=row[2],
        )

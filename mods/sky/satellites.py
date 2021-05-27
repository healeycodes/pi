from db import connect, close, FORMAT_STRING as F
from datetime import datetime
from dataclasses import dataclass

# https://en.wikipedia.org/wiki/List_of_GPS_satellites
PRN_DESCRIPTIONS = {
    "13": "USA-132",
    "20": "USA-150",
    "28": "USA-151",
    "16": "USA-166",
    "21": "USA-168",
    "22": "USA-175",
    "19": "USA-177",
    "02": "USA-180",
    "17": "USA-183",
    "31": "USA-190",
    "12": "USA-192",
    "15": "USA-196",
    "29": "USA-199",
    "07": "USA-201",
    "05": "USA-206",
    "25": "USA-213",
    "01": "USA-232",
    "24": "USA-239",
    "27": "USA-242",
    "30": "USA-248",
    "06": "USA-251",
    "09": "USA-256",
    "03": "USA-258",
    "26": "USA-260",
    "08": "USA-262",
    "10": "USA-265",
    "32": "USA-266",
    "04": "USA-289 Vespucci",
    "18": "USA-293 Magellan",
    "23": "USA-304 Matthew Henson",
    "14": "USA-309 Sacagawea",
}


@dataclass
class Satellite:
    prn: str
    description: str
    status: int
    timestamp: str


def save_sats(sats):
    # TODO: optimize this SQL once we've settled on a SQL language
    connection, cursor = connect()
    cursor.execute(
        f"UPDATE satellites SET status=0, timestamp={F} WHERE status=1",
        (datetime.now(),),
    )
    for prn in sats:
        cursor.execute(f"SELECT prn FROM satellites WHERE prn={F} LIMIT 1", (prn,))
        if not cursor.fetchone():
            desc = PRN_DESCRIPTIONS[prn] if prn in PRN_DESCRIPTIONS else "Unknown"
            cursor.execute(
                f"INSERT INTO satellites (prn, status, description, timestamp) VALUES ({F}, {F}, {F}, {F})",
                (prn, 1, desc, datetime.now(),),
            )
        else:
            cursor.execute(
                f"UPDATE satellites SET status=1, timestamp={F} WHERE prn={F} and status=0",
                (datetime.now(), prn,),
            )
    close(connection)


def get_sats():
    connection, cursor = connect()
    cursor.execute("SELECT prn, description, status, timestamp FROM satellites")
    rows = cursor.fetchall()
    close(connection)
    return [
        Satellite(prn=row[0], description=row[1], status=row[2], timestamp=row[3])
        for row in rows
    ]

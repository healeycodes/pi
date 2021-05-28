import json


def test_sky(client):

    # send two satellite prns
    rv = client.get("/sky/send?sats=01,02")
    assert rv.status_code == 200

    rv = client.get("/sky/get")
    json_data = json.loads(rv.data)
    json_data.sort(key=lambda sat: int(sat["prn"]))

    assert json_data[0]["prn"] == "01"
    assert json_data[0]["status"] == 1
    assert json_data[0]["description"] == "USA-232"
    assert "timestamp" in json_data[0]

    assert json_data[1]["prn"] == "02"
    assert json_data[1]["status"] == 1
    assert json_data[1]["description"] == "USA-180"
    assert "timestamp" in json_data[1]

    # on the next update, 01 is not available
    # so its status should be 0 as in: seen before but not visible
    rv = client.get("/sky/send?sats=02,03")
    assert rv.status_code == 200

    rv = client.get("/sky/get")
    json_data = json.loads(rv.data)
    json_data.sort(key=lambda sat: int(sat["prn"]))

    assert json_data[0]["prn"] == "01"
    assert json_data[0]["status"] == 0

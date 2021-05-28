import json


def test_weather(client):

    rv = client.get("/weather/send?temperature=12.2&humidity=32.2")
    assert rv.status_code == 200

    rv = client.get("/weather/get")
    json_data = json.loads(rv.data)
    assert json_data["temperature"] == 12.2
    assert json_data["humidity"] == 32.2
    assert "timestamp" in json_data

def test_home_web_page(client):
    rv = client.get("/")
    assert rv.status_code == 302

    rv = client.get("/home/")
    assert rv.status_code == 200

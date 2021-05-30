import json


def test_printer_no_new_messages(client):
    rv = client.get("/printer/get-msg")
    assert rv.status_code == 204


def test_printer_example_use_case(client):

    # send two messages to the print queue
    rv = client.get("/printer/put-msg?text=printme1")
    assert rv.status_code == 200

    rv = client.get("/printer/put-msg?text=printme2")
    assert rv.status_code == 200

    rv = client.get("/printer/get-msg")
    msg_one = json.loads(rv.data)
    assert msg_one["text"] == "printme1"
    assert "name" in msg_one

    # check status is reported correctly
    # `queued` turns into `printed` after the confirmation
    rv = client.get(f"/printer/check-msg?msg_id={msg_one['msg_id']}")
    msg_one_check = json.loads(rv.data)
    assert "queued" in msg_one_check["status"]

    rv = client.get(f"/printer/confirm-msg?msg_id={msg_one['msg_id']}")
    assert rv.status_code == 200

    rv = client.get(f"/printer/check-msg?msg_id={msg_one['msg_id']}")
    msg_one_check = json.loads(rv.data)
    assert "printed" in msg_one_check["status"]

    # the newest message is available to print next
    rv = client.get("/printer/get-msg")
    msg_two = json.loads(rv.data)
    assert msg_two["text"] == "printme2"

from flask import request


def get_remote_address():
    if "X-Forwarded-For" in request.headers:
        return request.headers.getlist("X-Forwarded-For")[0].rpartition(" ")[-1]
    else:
        return request.remote_addr or "untrackable"

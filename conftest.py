import os
import pytest
import tempfile


@pytest.fixture
def client():
    db_fd, os.environ["TEST_DB"] = tempfile.mkstemp()

    from server import create_app

    app = create_app()
    with app.test_client() as client:
        yield client

    os.close(db_fd)
    # os.unsetenv("TEST_DB")

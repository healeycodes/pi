from server import create_app
from server.db import get_db

get_db().setup()
app = create_app()

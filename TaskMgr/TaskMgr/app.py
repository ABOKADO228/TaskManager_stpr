import os
import sys
import bottle
from bottle import TEMPLATE_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, "views"))

PROJECT_ROOT = BASE_DIR
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

import routes

if "--debug" in sys.argv[1:] or "SERVER_DEBUG" in os.environ:
    bottle.debug(True)

@bottle.route("/static/<filepath:path>")
def server_static(filepath):
    return bottle.static_file(filepath, root=STATIC_ROOT)

if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 5555

    bottle.run(server="wsgiref", host=HOST, port=PORT, debug=True, reloader=True)
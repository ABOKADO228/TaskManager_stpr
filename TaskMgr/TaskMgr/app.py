"""
This script runs the application using a development server.
"""

import os
import sys
import bottle
from bottle import TEMPLATE_PATH

# 1) СНАЧАЛА настраиваем пути

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ...\TaskMgr\TaskMgr
TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, "views"))

PROJECT_ROOT = BASE_DIR
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# 2) ПОТОМ импортируем routes (они уже увидят TEMPLATE_PATH)

import routes  # noqa: E402

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
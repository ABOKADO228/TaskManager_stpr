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

# Отдает статические файлы проекта: CSS, JavaScript, шрифты и изображения.
# @param filepath относительный путь к файлу внутри папки static.
# @returns HTTP-ответ Bottle с содержимым найденного статического файла.
# @throws HTTPError Bottle вернет 404, если файл не найден в STATIC_ROOT.
# @note все CSS-точки входа и импортируемые CSS-файлы загружаются через этот маршрут.
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

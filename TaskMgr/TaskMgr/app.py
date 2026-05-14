import os
import sys

import bottle
from bottle import TEMPLATE_PATH


# Определяет основные папки проекта.
# @returns значения BASE_DIR, TEMPLATE_PATH и STATIC_ROOT используются Bottle при запуске.
# @throws не выбрасывает исключения напрямую.
# @note путь строится от app.py, поэтому сервер можно запускать из разных рабочих папок.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, "views"))
STATIC_ROOT = os.path.join(BASE_DIR, "static")


import routes

# Включает debug-режим Bottle.
# @returns None.
# @note debug можно включить аргументом --debug или переменной окружения SERVER_DEBUG.
if "--debug" in sys.argv[1:] or "SERVER_DEBUG" in os.environ:
    bottle.debug(True)

# Запускает локальный сервер разработки.
# @returns None.
# @throws ValueError порта обрабатывается и заменяется значением по умолчанию.
# @note блок выполняется только при прямом запуске app.py.
if __name__ == "__main__":
    host = os.environ.get("SERVER_HOST", "0.0.0.0")

    try:
        port = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        port = 5555

# Обязательная функция для поиска ресурсов в проекте
    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        return bottle.static_file(filepath, root=STATIC_ROOT)

    bottle.run(server="wsgiref", host=host, port=port, debug=True, reloader=True)

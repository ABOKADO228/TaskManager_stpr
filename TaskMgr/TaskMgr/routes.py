# Маршруты и представления Bottle-приложения.

import json
from datetime import date
from urllib.parse import unquote

from bottle import HTTPResponse, redirect, request, route, view

from auth_service import (
    build_user,
    find_user_by_username,
    load_users,
    normalize_username,
    public_user_view,
    save_users,
    validate_registration_form,
)
from active_user_service import (
    build_active_user,
    empty_user_form,
    load_all_users,
    load_active_users,
    save_active_users,
    validate_active_user,
)
from order_service import (
    build_order,
    empty_form,
    load_orders,
    load_orders_for_user,
    save_orders,
    validate_order,
)


def json_response(payload, status=200):
    return HTTPResponse(
        body=json.dumps(payload, ensure_ascii=False),
        status=status,
        content_type="application/json",
    )


def read_auth_payload():
    json_payload = request.json if isinstance(request.json, dict) else {}
    if json_payload:
        return json_payload

    return {
        "display_name": request.forms.getunicode("display_name") or "",
        "username": request.forms.getunicode("username") or "",
        "password": request.forms.getunicode("password") or "",
        "password_repeat": request.forms.getunicode("password_repeat") or "",
    }


# Получает пользователя из cookie, созданной страницей входа.
# @returns словарь текущего пользователя или None, если пользователь не авторизован.
# @throws не выбрасывает исключения напрямую.
# @note Bottle не видит localStorage, поэтому для серверной защиты /orders используется cookie taskmgr_user_id.
def get_current_user():
    user_id = request.get_cookie("taskmgr_user_id")
    if not user_id:
        return None

    username = unquote(request.get_cookie("taskmgr_username") or "")
    display_name = unquote(request.get_cookie("taskmgr_display_name") or username)

    return {
        "id": unquote(user_id),
        "username": username,
        "display_name": display_name or username,
    }


# Отображает стартовую страницу сайта.
# @returns словарь контекста для шаблона views/index.tpl.
# @throws не выбрасывает исключения напрямую.
# @note страница содержит навигацию к входу, заказам и активным пользователям.
@route("/")
@view("index")
def home():
    return {}


# Отображает главное рабочее пространство пользователя.
# @returns словарь контекста для шаблона views/main.tpl.
# @throws не выбрасывает исключения напрямую.
# @note доступ дополнительно проверяется клиентским JavaScript через localStorage.
@route("/main")
@view("./main")
def main():
    return {}


# Отображает страницу входа и регистрации.
# @returns словарь контекста для шаблона views/reg-auth.tpl.
# @throws не выбрасывает исключения напрямую.
# @note в текущем прототипе регистрация и вход проходят через JSON-эндпоинты на этом же сервере.
@route("/reg-auth")
@view("./reg-auth")
def reg_auth():
    return {}


@route("/api/auth/login", method="POST")
def api_login():
    form = read_auth_payload()
    username = normalize_username(form.get("username"))
    password = str(form.get("password") or "")

    if not username or not password:
        return json_response({"ok": False, "message": "Введите логин и пароль."}, 400)

    user = find_user_by_username(load_users(), username)
    if not user or user.get("password") != password:
        return json_response({"ok": False, "message": "Неверный логин или пароль."}, 401)

    return json_response({"ok": True, "user": public_user_view(user)})


@route("/api/auth/register", method="POST")
def api_register():
    form = read_auth_payload()
    users = load_users()
    errors = validate_registration_form(form, users)

    if errors:
        return json_response({"ok": False, "errors": errors}, 400)

    user = build_user(form)
    users.append(user)
    save_users(users)

    return json_response({"ok": True, "user": public_user_view(user)})


# Отображает страницу оформленных заказов с чистой формой добавления.
# @returns контекст шаблона views/orders.tpl: список заказов, ошибки и состояние формы.
# @throws не выбрасывает исключения напрямую; чтение JSON защищено в load_orders.
# @note заказы показываются только текущему пользователю по owner_id.
@route("/orders", method="GET")
@view("orders")
def orders_page():
    current_user = get_current_user()
    if not current_user:
        redirect("/reg-auth?next=/orders")

    user_orders = load_orders_for_user(current_user["id"])

    return {
        "orders": user_orders,
        "errors": {},
        "form": empty_form(),
        "current_user": current_user,
        "today": date.today().isoformat(),
        "saved": request.query.get("saved") == "1",
    }


# Обрабатывает отправку формы нового оформленного заказа.
# @returns контекст страницы с ошибками либо redirect на /orders при успехе.
# @throws OSError если save_orders не сможет записать JSON-файл.
# @note redirect после успешного POST очищает форму и защищает от повторной отправки.
@route("/orders", method="POST")
@view("orders")
def add_order():
    current_user = get_current_user()
    if not current_user:
        redirect("/reg-auth?next=/orders")

    form = {
        "number": (request.forms.getunicode("number") or "").strip(),
        "author": (request.forms.getunicode("author") or "").strip(),
        "text": (request.forms.getunicode("text") or "").strip(),
        "date": (request.forms.getunicode("date") or "").strip(),
        "phone": (request.forms.getunicode("phone") or "").strip(),
    }

    all_orders = load_orders()
    user_orders = load_orders_for_user(current_user["id"])
    errors = validate_order(form, user_orders)

    if errors:
        return {
            "orders": user_orders,
            "errors": errors,
            "form": form,
            "current_user": current_user,
            "today": date.today().isoformat(),
            "saved": False,
        }

    new_order = build_order(form, current_user)
    all_orders.append(new_order)
    save_orders(all_orders)
    redirect("/orders?saved=1")


# Отображает страницу активных пользователей.
# @returns контекст шаблона views/active-users.tpl: список пользователей, ошибки и форма.
# @throws не выбрасывает исключения напрямую; чтение JSON защищено в load_active_users.
# @note это страница варианта 6 по заданию.
@route("/active-users", method="GET")
@view("active-users")
def active_users_page():
    return {
        "users": load_active_users(),
        "errors": {},
        "form": empty_user_form(),
        "today": date.today().isoformat(),
        "saved": request.query.get("saved") == "1",
    }


# Обрабатывает отправку формы нового активного пользователя.
# @returns контекст страницы с ошибками либо redirect на /active-users при успехе.
# @throws OSError если save_active_users не сможет записать JSON-файл.
# @note серверная валидация работает даже при отключенной HTML5-валидации браузера.
@route("/active-users", method="POST")
@view("active-users")
def add_active_user():
    form = {
        "nick": (request.forms.getunicode("nick") or "").strip(),
        "description": (request.forms.getunicode("description") or "").strip(),
        "active_date": (request.forms.getunicode("active_date") or "").strip(),
        "phone": (request.forms.getunicode("phone") or "").strip(),
        "events_created": (request.forms.getunicode("events_created") or "").strip(),
        "comments_count": (request.forms.getunicode("comments_count") or "").strip(),
        "notes_count": (request.forms.getunicode("notes_count") or "").strip(),
        "groups_joined": (request.forms.getunicode("groups_joined") or "").strip(),
    }

    all_users = load_all_users()
    errors = validate_active_user(form, all_users)

    if errors:
        return {
            "users": load_active_users(),
            "errors": errors,
            "form": form,
            "today": date.today().isoformat(),
            "saved": False,
        }

    new_user = build_active_user(form)
    all_users.append(new_user)
    save_active_users(all_users)
    redirect("/active-users?saved=1")

# Маршруты и представления Bottle-приложения.

from bottle import redirect, request, route, view

from active_user_service import (
    build_active_user,
    empty_user_form,
    load_active_users,
    save_active_users,
    validate_active_user,
)
from order_service import build_order, empty_form, load_orders, save_orders, validate_order


# Отображает стартовую страницу сайта.
# @returns словарь контекста для шаблона views/index.tpl.
# @throws не выбрасывает исключения напрямую.
# @note страница содержит навигацию к входу, заказам и активным пользователям.
@route('/')
@view('index')
def home():
    return dict()


# Отображает главное рабочее пространство пользователя.
# @returns словарь контекста для шаблона views/main.tpl.
# @throws не выбрасывает исключения напрямую.
# @note доступ дополнительно проверяется клиентским JavaScript через localStorage.
# FIXME проверку авторизации нужно перенести на серверную сторону.
@route('/main')
@view('./main')
def main():
    return dict()


# Отображает страницу входа и регистрации.
# @returns словарь контекста для шаблона views/reg-auth.tpl.
# @throws не выбрасывает исключения напрямую.
# @note в текущем прототипе регистрация и вход реализованы на клиенте.
# FIXME пароли и сессии нужно перенести на backend перед реальным использованием.
@route('/reg-auth')
@view('./reg-auth')
def reg_auth():
    return dict()


# Отображает страницу оформленных заказов с чистой формой добавления.
# @returns контекст шаблона views/orders.tpl: список заказов, ошибки и состояние формы.
# @throws не выбрасывает исключения напрямую; чтение JSON защищено в load_orders.
# @note заказы загружаются из файла Python-кодом и сортируются по дате.
@route('/orders', method='GET')
@view('orders')
def orders_page():
    return {
        "orders": load_orders(),
        "errors": {},
        "form": empty_form(),
    }


# Обрабатывает отправку формы нового оформленного заказа.
# @returns контекст страницы с ошибками либо redirect на /orders при успехе.
# @throws OSError если save_orders не сможет записать JSON-файл.
# @note redirect после успешного POST очищает форму и защищает от повторной отправки.
@route('/orders', method='POST')
@view('orders')
def add_order():
    # Копируем только ожидаемые поля, чтобы лишние данные не попали в JSON.
    form = {
        "number": (request.forms.getunicode("number") or "").strip(),
        "author": (request.forms.getunicode("author") or "").strip(),
        "text": (request.forms.getunicode("text") or "").strip(),
        "date": (request.forms.getunicode("date") or "").strip(),
        "phone": (request.forms.getunicode("phone") or "").strip(),
    }

    orders = load_orders()
    errors = validate_order(form, orders)

    if errors:
        return {
            "orders": orders,
            "errors": errors,
            "form": form,
        }

    orders.append(build_order(form))
    save_orders(orders)
    redirect('/orders')


# Отображает страницу активных пользователей.
# @returns контекст шаблона views/active-users.tpl: список пользователей, ошибки и форма.
# @throws не выбрасывает исключения напрямую; чтение JSON защищено в load_active_users.
# @note это страница варианта 6 по заданию.
@route('/active-users', method='GET')
@view('active-users')
def active_users_page():
    return {
        "users": load_active_users(),
        "errors": {},
        "form": empty_user_form(),
    }


# Обрабатывает отправку формы нового активного пользователя.
# @returns контекст страницы с ошибками либо redirect на /active-users при успехе.
# @throws OSError если save_active_users не сможет записать JSON-файл.
# @note серверная валидация работает даже при отключенной HTML5-валидации браузера.
@route('/active-users', method='POST')
@view('active-users')
def add_active_user():
    # Копируем только ожидаемые поля, чтобы структура JSON оставалась предсказуемой.
    form = {
        "nick": (request.forms.getunicode("nick") or "").strip(),
        "description": (request.forms.getunicode("description") or "").strip(),
        "active_date": (request.forms.getunicode("active_date") or "").strip(),
        "phone": (request.forms.getunicode("phone") or "").strip(),
    }

    users = load_active_users()
    errors = validate_active_user(form, users)

    if errors:
        return {
            "users": users,
            "errors": errors,
            "form": form,
        }

    users.append(build_active_user(form))
    save_active_users(users)
    redirect('/active-users')

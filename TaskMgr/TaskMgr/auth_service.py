from copy import deepcopy
from pathlib import Path
import json
import re
import uuid


DEFAULT_USERS = [
    {
        "id": "user-admin",
        "username": "admin",
        "displayName": "Администратор",
        "password": "1234",
    },
    {
        "id": "user-user1",
        "username": "user1",
        "displayName": "Пользователь",
        "password": "1111",
    },
]

USERNAME_PATTERN = re.compile(r"^[a-z0-9._-]+$")

# Возвращает полный путь до файла для записи пользователей.
# @returns полный путь до файла для записи пользователей.
def default_users_path():
    return Path(__file__).resolve().parent / "data" / "users.json"

# Приводит имя пользователя в нормальный вид.
# @param value строка подлежащая нормализации.
# @returns имя пользователя в нормальном виде.
def normalize_username(value):
    return str(value or "").strip().lower()


def normalize_display_name(value):
    return str(value or "").strip()


def load_users(path=None):
    users_path = Path(path) if path else default_users_path()

    if not users_path.exists():
        return deepcopy(DEFAULT_USERS)

    try:
        with users_path.open("r", encoding="utf-8") as file:
            users = json.load(file)
    except (OSError, json.JSONDecodeError):
        return deepcopy(DEFAULT_USERS)

    if not isinstance(users, list):
        return deepcopy(DEFAULT_USERS)

    valid_users = []
    for user in users:
        if not isinstance(user, dict):
            continue
        username = normalize_username(user.get("username"))
        display_name = normalize_display_name(user.get("displayName"))
        password = str(user.get("password") or "")
        user_id = str(user.get("id") or "")

        if not username or not display_name or not password or not user_id:
            continue

        valid_users.append(
            {
                "id": user_id,
                "username": username,
                "displayName": display_name,
                "password": password,
            }
        )

    return valid_users or deepcopy(DEFAULT_USERS)


def save_users(users, path=None):
    users_path = Path(path) if path else default_users_path()
    users_path.parent.mkdir(parents=True, exist_ok=True)

    with users_path.open("w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)


def find_user_by_username(users, username):
    normalized_username = normalize_username(username)
    if not normalized_username:
        return None

    for user in users:
        if normalize_username(user.get("username")) == normalized_username:
            return user
    return None


def is_valid_username(username):
    return bool(USERNAME_PATTERN.fullmatch(normalize_username(username)))


def validate_registration_form(form, existing_users):
    errors = {}
    display_name = normalize_display_name(form.get("display_name"))
    username = normalize_username(form.get("username"))
    password = str(form.get("password") or "")
    password_repeat = str(form.get("password_repeat") or "")

    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!\.%*?&])[A-Za-z\d@$\.!%*?&]{8,}$"

    if not display_name:
        errors["display_name"] = "Введите имя."

    if not username:
        errors["username"] = "Введите логин."
    elif not is_valid_username(username):
        errors["username"] = "Логин может содержать только латиницу, цифры, точку, дефис и подчёркивание."
    elif find_user_by_username(existing_users, username):
        errors["username"] = "Такой логин уже занят."

    if not password:
        errors["password"] = "Введите пароль."
    elif len(password) < 8:
        errors["password"] = "Пароль должен быть не короче 8 символов."
    elif password != password.strip():
        errors["password"] = "Пароль не должен начинаться или заканчиваться пробелом."
    elif not re.match(password_regex, password):
        errors["password"] = "Пароль слишком простой: добавьте заглавную букву, цифру и спецсимвол (@$!%*?&)."

    if not password_repeat:
        errors["password_repeat"] = "Повторите пароль."
    elif password and password_repeat != password:
        errors["password_repeat"] = "Пароли не совпадают."

    return errors


def build_user(form):
    return {
        "id": f"user-{uuid.uuid4().hex[:12]}",
        "username": normalize_username(form.get("username")),
        "displayName": normalize_display_name(form.get("display_name")),
        "password": str(form.get("password") or ""),
    }


def public_user_view(user):
    return {
        "id": user["id"],
        "username": user["username"],
        "displayName": user["displayName"],
    }

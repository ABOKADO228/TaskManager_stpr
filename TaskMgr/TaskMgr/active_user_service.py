# Модуль содержит бизнес-логику страницы "Активные пользователи".
# Он не зависит от Bottle напрямую, поэтому эти функции удобно тестировать.

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path


# Формат даты, который отправляет браузерное поле input[type="date"].
DATE_FORMAT = "%Y-%m-%d"

# Регулярное выражение допускает российский телефон с пробелами, скобками
# и дефисами. Точное количество цифр проверяется отдельно.
PHONE_PATTERN = re.compile(r"^\+?[\d\s()\-]{10,20}$")


# Возвращает стандартный путь к JSON-файлу активных пользователей.
# @returns путь к файлу data/active_users.json.
# @throws не выбрасывает исключения напрямую.
# @note путь строится относительно этого файла, а не текущей рабочей папки.
def default_active_users_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "active_users.json"


# Создает пустое состояние формы активного пользователя.
# @returns словарь с пустыми значениями для всех полей формы.
# @throws не выбрасывает исключения.
# @note ключи должны совпадать с name-полями в views/active-users.tpl.
def empty_user_form() -> dict[str, str]:
    return {
        "nick": "",
        "description": "",
        "active_date": "",
        "phone": "",
    }


# Загружает активных пользователей из JSON-файла.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns список пользователей, отсортированный по дате активности от новых к старым.
# @throws не выбрасывает исключения наружу; ошибки чтения и JSON обрабатываются внутри.
# @note пустой список возвращается, если файл отсутствует или поврежден.
# FIXME для production нужно логировать поврежденный JSON и ошибки доступа к файлу.
def load_active_users(path: Path | None = None) -> list[dict[str, str]]:
    users_path = path or default_active_users_path()
    if not users_path.exists():
        return []

    try:
        with users_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(loaded, list):
        return []

    return sorted(loaded, key=lambda item: item.get("active_date", ""), reverse=True)


# Сохраняет активных пользователей в JSON-файл.
# @param users список пользователей для записи.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns None.
# @throws OSError если папку или файл не удалось создать/записать.
# @note ensure_ascii=False нужен, чтобы русские строки оставались читаемыми.
def save_active_users(users: list[dict[str, str]], path: Path | None = None) -> None:
    users_path = path or default_active_users_path()
    users_path.parent.mkdir(parents=True, exist_ok=True)

    with users_path.open("w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)


# Проверяет дату активности пользователя.
# @param value строка даты из формы в формате YYYY-MM-DD.
# @returns True, если дата корректна и не позже сегодняшнего дня; иначе False.
# @throws не выбрасывает исключения; ValueError при парсинге даты перехватывается.
# @note будущие даты запрещены, потому что список хранит уже активных пользователей.
def is_valid_activity_date(value: str) -> bool:
    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return False

    return parsed <= date.today()


# Проверяет телефон активного пользователя.
# @param value телефон, введенный в форму.
# @returns True, если телефон содержит 11 цифр и начинается с 7 или 8; иначе False.
# @throws не выбрасывает исключения.
# @note формат допускает пробелы, скобки и дефисы, но хранится исходная строка.
# FIXME при подключении БД стоит нормализовать телефон к единому виду +79991234567.
def is_valid_user_phone(value: str) -> bool:
    if not PHONE_PATTERN.match(value):
        return False

    digits = re.sub(r"\D", "", value)
    return len(digits) == 11 and digits[0] in {"7", "8"}


# Проверяет форму добавления активного пользователя.
# @param form словарь с полями nick, description, active_date, phone.
# @param existing_users уже сохраненные пользователи для проверки уникальности ника.
# @returns словарь ошибок вида {имя_поля: текст_ошибки}; пустой словарь означает успех.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note имена ключей ошибок совпадают с именами HTML-полей для вывода рядом с input.
def validate_active_user(form: dict[str, str], existing_users: list[dict[str, str]]) -> dict[str, str]:
    errors: dict[str, str] = {}

    nick = form["nick"].strip()
    description = form["description"].strip()
    active_date = form["active_date"].strip()
    phone = form["phone"].strip()

    if not nick:
        errors["nick"] = "Введите ник активного пользователя."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё0-9_.-]{3,24}$", nick):
        errors["nick"] = "Ник должен содержать 3-24 символа: буквы, цифры, точку, дефис или подчеркивание."
    elif any(user.get("nick", "").lower() == nick.lower() for user in existing_users):
        errors["nick"] = "Пользователь с таким ником уже есть в списке."

    if not description:
        errors["description"] = "Добавьте описание активности пользователя."
    elif len(description) < 10:
        errors["description"] = "Описание должно быть не короче 10 символов."

    if not active_date:
        errors["active_date"] = "Укажите дату активности."
    elif not is_valid_activity_date(active_date):
        errors["active_date"] = "Дата должна быть в формате ГГГГ-ММ-ДД и не позже сегодняшнего дня."

    if not phone:
        errors["phone"] = "Укажите телефон."
    elif not is_valid_user_phone(phone):
        errors["phone"] = "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX."

    return errors


# Создает объект активного пользователя из проверенной формы.
# @param form валидный словарь формы с полями nick, description, active_date, phone.
# @returns словарь активного пользователя для сохранения в JSON.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note функцию нужно вызывать только после validate_active_user.
def build_active_user(form: dict[str, str]) -> dict[str, str]:
    return {
        "nick": form["nick"].strip(),
        "description": form["description"].strip(),
        "active_date": form["active_date"].strip(),
        "phone": form["phone"].strip(),
    }

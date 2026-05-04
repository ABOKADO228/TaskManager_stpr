# Модуль содержит бизнес-логику страницы "Оформленные заказы".
# Функции отделены от Bottle, чтобы их можно было проверять unit-тестами.

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


# Возвращает стандартный путь к JSON-файлу оформленных заказов.
# @returns путь к файлу data/orders.json.
# @throws не выбрасывает исключения напрямую.
# @note путь строится относительно этого файла, а не текущей рабочей папки.
def default_orders_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "orders.json"


# Создает пустое состояние формы заказа.
# @returns словарь с пустыми значениями для всех полей формы заказа.
# @throws не выбрасывает исключения.
# @note используется при первом открытии страницы и после успешного redirect.
def empty_form() -> dict[str, str]:
    return {
        "number": "",
        "author": "",
        "text": "",
        "date": "",
        "phone": "",
    }


# Загружает оформленные заказы из JSON-файла.
# @param path путь к JSON-файлу; если None, используется data/orders.json.
# @returns список заказов, отсортированный по дате от новых к старым.
# @throws не выбрасывает исключения наружу; ошибки чтения и JSON обрабатываются внутри.
# @note пустой список возвращается, если файл отсутствует или поврежден.
# FIXME для production нужно заменить JSON на БД и логировать ошибки чтения.
def load_orders(path: Path | None = None) -> list[dict[str, str]]:
    orders_path = path or default_orders_path()
    if not orders_path.exists():
        return []

    try:
        with orders_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(loaded, list):
        return []

    return sorted(loaded, key=lambda item: item.get("date", ""), reverse=True)


# Сохраняет оформленные заказы в JSON-файл.
# @param orders список заказов для записи.
# @param path путь к JSON-файлу; если None, используется data/orders.json.
# @returns None.
# @throws OSError если папку или файл не удалось создать/записать.
# @note ensure_ascii=False нужен, чтобы русские строки оставались читаемыми.
def save_orders(orders: list[dict[str, str]], path: Path | None = None) -> None:
    orders_path = path or default_orders_path()
    orders_path.parent.mkdir(parents=True, exist_ok=True)

    with orders_path.open("w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=2)


# Проверяет дату оформления заказа.
# @param value строка даты из формы в формате YYYY-MM-DD.
# @returns True, если дата корректна и не позже сегодняшнего дня; иначе False.
# @throws не выбрасывает исключения; ValueError при парсинге даты перехватывается.
# @note будущие даты запрещены, потому что список хранит уже оформленные заказы.
def is_valid_order_date(value: str) -> bool:
    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return False

    return parsed <= date.today()


# Проверяет телефон заказа.
# @param value телефон, введенный в форму заказа.
# @returns True, если телефон содержит 11 цифр и начинается с 7 или 8; иначе False.
# @throws не выбрасывает исключения.
# @note формат допускает пробелы, скобки и дефисы, но хранится исходная строка.
def is_valid_phone(value: str) -> bool:
    if not PHONE_PATTERN.match(value):
        return False

    digits = re.sub(r"\D", "", value)
    return len(digits) == 11 and digits[0] in {"7", "8"}


# Проверяет форму добавления оформленного заказа.
# @param form словарь с полями number, author, text, date, phone.
# @param existing_orders уже сохраненные заказы для проверки уникальности номера.
# @returns словарь ошибок вида {имя_поля: текст_ошибки}; пустой словарь означает успех.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note имена ключей ошибок совпадают с именами HTML-полей для вывода рядом с input.
def validate_order(form: dict[str, str], existing_orders: list[dict[str, str]]) -> dict[str, str]:
    errors: dict[str, str] = {}

    number = form["number"].strip()
    author = form["author"].strip()
    text = form["text"].strip()
    order_date = form["date"].strip()
    phone = form["phone"].strip()

    if not number:
        errors["number"] = "Введите номер заказа."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё0-9\-]{3,20}$", number):
        errors["number"] = "Номер должен содержать 3-20 символов: буквы, цифры или дефис."
    elif any(order.get("number", "").lower() == number.lower() for order in existing_orders):
        errors["number"] = "Заказ с таким номером уже есть в списке."

    if not author:
        errors["author"] = "Введите имя автора или клиента."
    elif len(author) < 2:
        errors["author"] = "Имя должно быть не короче 2 символов."

    if not text:
        errors["text"] = "Добавьте описание заказа."
    elif len(text) < 10:
        errors["text"] = "Описание должно быть не короче 10 символов."

    if not order_date:
        errors["date"] = "Укажите дату заказа."
    elif not is_valid_order_date(order_date):
        errors["date"] = "Дата должна быть в формате ГГГГ-ММ-ДД и не позже сегодняшнего дня."

    if not phone:
        errors["phone"] = "Укажите телефон."
    elif not is_valid_phone(phone):
        errors["phone"] = "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX."

    return errors


# Создает объект заказа из проверенной формы.
# @param form валидный словарь формы с полями number, author, text, date, phone.
# @returns словарь заказа для сохранения в JSON.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note функцию нужно вызывать только после validate_order.
def build_order(form: dict[str, str]) -> dict[str, str]:
    return {
        "number": form["number"].strip(),
        "author": form["author"].strip(),
        "text": form["text"].strip(),
        "date": form["date"].strip(),
        "phone": form["phone"].strip(),
    }

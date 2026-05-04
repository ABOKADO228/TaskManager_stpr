"""Utility functions for the оформленные заказы page.

The module is intentionally framework-light: routes use it, and unit tests can
validate input rules without starting the Bottle server.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path


# The date field uses one predictable browser-friendly format.
DATE_FORMAT = "%Y-%m-%d"

# Phone is accepted in common Russian formats: +79991234567, 89991234567,
# +7 (999) 123-45-67. We normalize only by checking digits, not by rewriting.
PHONE_PATTERN = re.compile(r"^\+?[\d\s()\-]{10,20}$")


def default_orders_path() -> Path:
    """Return the default JSON file used by the application."""

    return Path(__file__).resolve().parent / "data" / "orders.json"


def empty_form() -> dict[str, str]:
    """Create a clean form state for the Bottle template."""

    return {
        "number": "",
        "author": "",
        "text": "",
        "date": "",
        "phone": "",
    }


def load_orders(path: Path | None = None) -> list[dict[str, str]]:
    """Load orders from JSON and sort the freshest orders first."""

    orders_path = path or default_orders_path()
    if not orders_path.exists():
        return []

    try:
        with orders_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        # If the file is temporarily unavailable or corrupted, the page should
        # still open. In a production project this branch should be logged.
        return []

    if not isinstance(loaded, list):
        return []

    return sorted(loaded, key=lambda item: item.get("date", ""), reverse=True)


def save_orders(orders: list[dict[str, str]], path: Path | None = None) -> None:
    """Persist orders to a JSON file with UTF-8 text."""

    orders_path = path or default_orders_path()
    orders_path.parent.mkdir(parents=True, exist_ok=True)

    with orders_path.open("w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=2)


def is_valid_order_date(value: str) -> bool:
    """Validate a YYYY-MM-DD date and reject future dates."""

    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return False

    return parsed <= date.today()


def is_valid_phone(value: str) -> bool:
    """Validate Russian phone input by format and digit count."""

    if not PHONE_PATTERN.match(value):
        return False

    digits = re.sub(r"\D", "", value)
    return len(digits) == 11 and digits[0] in {"7", "8"}


def validate_order(form: dict[str, str], existing_orders: list[dict[str, str]]) -> dict[str, str]:
    """Return validation errors for an order form."""

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


def build_order(form: dict[str, str]) -> dict[str, str]:
    """Convert a validated form dictionary into an order item."""

    return {
        "number": form["number"].strip(),
        "author": form["author"].strip(),
        "text": form["text"].strip(),
        "date": form["date"].strip(),
        "phone": form["phone"].strip(),
    }

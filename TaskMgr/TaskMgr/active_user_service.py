"""Business logic for the active users page.

The Bottle route uses these functions to read/write a JSON file, while unit
tests use the same validation rules without starting the web server.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path


# Browser date input sends values in this exact format.
DATE_FORMAT = "%Y-%m-%d"

# The page accepts Russian phone numbers with optional spaces, brackets and
# hyphens. Digit count is checked separately after removing formatting.
PHONE_PATTERN = re.compile(r"^\+?[\d\s()\-]{10,20}$")


def default_active_users_path() -> Path:
    """Return the JSON file used as storage for active users."""

    return Path(__file__).resolve().parent / "data" / "active_users.json"


def empty_user_form() -> dict[str, str]:
    """Return an empty form state for the template."""

    return {
        "nick": "",
        "description": "",
        "active_date": "",
        "phone": "",
    }


def load_active_users(path: Path | None = None) -> list[dict[str, str]]:
    """Load active users from JSON and put the newest activity first."""

    users_path = path or default_active_users_path()
    if not users_path.exists():
        return []

    try:
        with users_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        # The page should not crash if a file is temporarily unreadable or
        # damaged. A real system would additionally log this exception.
        return []

    if not isinstance(loaded, list):
        return []

    return sorted(loaded, key=lambda item: item.get("active_date", ""), reverse=True)


def save_active_users(users: list[dict[str, str]], path: Path | None = None) -> None:
    """Save active users to a UTF-8 JSON file."""

    users_path = path or default_active_users_path()
    users_path.parent.mkdir(parents=True, exist_ok=True)

    with users_path.open("w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)


def is_valid_activity_date(value: str) -> bool:
    """Validate an activity date in YYYY-MM-DD format."""

    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return False

    return parsed <= date.today()


def is_valid_user_phone(value: str) -> bool:
    """Validate the active user's phone number."""

    if not PHONE_PATTERN.match(value):
        return False

    digits = re.sub(r"\D", "", value)
    return len(digits) == 11 and digits[0] in {"7", "8"}


def validate_active_user(form: dict[str, str], existing_users: list[dict[str, str]]) -> dict[str, str]:
    """Return field-specific validation errors for the active user form."""

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


def build_active_user(form: dict[str, str]) -> dict[str, str]:
    """Convert a validated form into a stored active user object."""

    return {
        "nick": form["nick"].strip(),
        "description": form["description"].strip(),
        "active_date": form["active_date"].strip(),
        "phone": form["phone"].strip(),
    }

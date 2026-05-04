# Модуль содержит бизнес-логику страницы "Активные пользователи".
# Активные пользователи не задаются вручную: они выбираются из общего списка
# существующих пользователей по расчетному рейтингу активности.

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path


# Формат даты, который отправляет браузерное поле input[type="date"].
DATE_FORMAT = "%Y-%m-%d"

# Минимальный рейтинг, после которого пользователь считается активным.
ACTIVE_SCORE_THRESHOLD = 10

# Регулярное выражение допускает российский телефон с пробелами, скобками
# и дефисами. Точное количество цифр проверяется отдельно.
PHONE_PATTERN = re.compile(r"^\+?[\d\s()\-]{10,20}$")


# Возвращает стандартный путь к JSON-файлу существующих пользователей.
# @returns путь к файлу data/active_users.json.
# @throws не выбрасывает исключения напрямую.
# @note файл хранит всех пользователей с метриками, а не только активных.
def default_active_users_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "active_users.json"


# Создает пустое состояние формы пользователя с метриками активности.
# @returns словарь с пустыми значениями для текстовых полей и нулями для метрик.
# @throws не выбрасывает исключения.
# @note ключи должны совпадать с name-полями в views/active-users.tpl.
def empty_user_form() -> dict[str, str]:
    return {
        "nick": "",
        "description": "",
        "active_date": "",
        "phone": "",
        "events_created": "0",
        "comments_count": "0",
        "notes_count": "0",
        "groups_joined": "0",
    }


# Безопасно преобразует значение метрики в неотрицательное целое число.
# @param value значение из формы или JSON-файла.
# @returns целое число больше или равно нулю.
# @throws не выбрасывает исключения; ошибки преобразования дают 0.
# @note функция нужна, чтобы поврежденные метрики в JSON не ломали рейтинг.
def parse_metric(value) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0

    return max(parsed, 0)


# Рассчитывает рейтинг активности пользователя.
# @param user пользователь с метриками events_created, comments_count, notes_count, groups_joined.
# @returns числовой рейтинг активности.
# @throws не выбрасывает исключения.
# @note события и комментарии имеют больший вес, потому что сильнее влияют на работу группы.
def calculate_activity_score(user: dict) -> int:
    events_score = parse_metric(user.get("events_created")) * 4
    comments_score = parse_metric(user.get("comments_count")) * 2
    notes_score = parse_metric(user.get("notes_count"))
    groups_score = parse_metric(user.get("groups_joined")) * 3
    recency_score = 2 if is_valid_activity_date(str(user.get("active_date", ""))) else 0

    return events_score + comments_score + notes_score + groups_score + recency_score


# Добавляет пользователю расчетный рейтинг активности.
# @param user пользователь из JSON-файла.
# @returns копию пользователя с полем activity_score.
# @throws не выбрасывает исключения.
# @note исходный словарь не изменяется, чтобы избежать неожиданных побочных эффектов.
def enrich_user_with_score(user: dict[str, str]) -> dict[str, str]:
    enriched = dict(user)
    enriched["activity_score"] = calculate_activity_score(user)
    return enriched


# Загружает всех пользователей из JSON-файла.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns список всех существующих пользователей без фильтрации по активности.
# @throws не выбрасывает исключения наружу; ошибки чтения и JSON обрабатываются внутри.
# @note используется для проверки уникальности и сохранения полного списка.
# FIXME для production нужно логировать поврежденный JSON и ошибки доступа к файлу.
def load_all_users(path: Path | None = None) -> list[dict[str, str]]:
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

    return loaded


# Загружает активных пользователей, выбранных из общего списка по рейтингу.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns список пользователей с activity_score, отсортированный по рейтингу и дате.
# @throws не выбрасывает исключения наружу; ошибки чтения обрабатываются в load_all_users.
# @note активным считается пользователь с рейтингом не ниже ACTIVE_SCORE_THRESHOLD.
def load_active_users(path: Path | None = None) -> list[dict[str, str]]:
    users = [enrich_user_with_score(user) for user in load_all_users(path)]
    active_users = [
        user
        for user in users
        if user["activity_score"] >= ACTIVE_SCORE_THRESHOLD
    ]

    return sorted(
        active_users,
        key=lambda item: (item.get("activity_score", 0), item.get("active_date", "")),
        reverse=True,
    )


# Сохраняет общий список существующих пользователей в JSON-файл.
# @param users список всех пользователей для записи.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns None.
# @throws OSError если папку или файл не удалось создать/записать.
# @note сохраняется полный список, а активные пользователи вычисляются при чтении.
def save_active_users(users: list[dict[str, str]], path: Path | None = None) -> None:
    users_path = path or default_active_users_path()
    users_path.parent.mkdir(parents=True, exist_ok=True)

    with users_path.open("w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)


# Проверяет дату последней активности пользователя.
# @param value строка даты из формы в формате YYYY-MM-DD.
# @returns True, если дата корректна и не позже сегодняшнего дня; иначе False.
# @throws не выбрасывает исключения; ValueError при парсинге даты перехватывается.
# @note будущие даты запрещены, потому что список хранит уже существующую активность.
def is_valid_activity_date(value: str) -> bool:
    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return False

    return parsed <= date.today()


# Проверяет телефон пользователя.
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


# Проверяет, что метрика активности является неотрицательным целым числом.
# @param value значение поля формы.
# @returns True, если значение можно сохранить как число больше или равно нулю.
# @throws не выбрасывает исключения.
# @note пустые значения не принимаются, чтобы рейтинг был однозначным.
def is_valid_metric(value: str) -> bool:
    if value == "":
        return False

    try:
        return int(value) >= 0
    except ValueError:
        return False


# Проверяет форму добавления существующего пользователя с метриками активности.
# @param form словарь с полями пользователя и метриками активности.
# @param existing_users уже сохраненные пользователи для проверки уникальности ника.
# @returns словарь ошибок вида {имя_поля: текст_ошибки}; пустой словарь означает успех.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note пользователь попадет в активные только если его расчетный рейтинг пройдет порог.
def validate_active_user(form: dict[str, str], existing_users: list[dict[str, str]]) -> dict[str, str]:
    errors: dict[str, str] = {}

    nick = form["nick"].strip()
    description = form["description"].strip()
    active_date = form["active_date"].strip()
    phone = form["phone"].strip()

    if not nick:
        errors["nick"] = "Введите ник пользователя."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё0-9_.-]{3,24}$", nick):
        errors["nick"] = "Ник должен содержать 3-24 символа: буквы, цифры, точку, дефис или подчеркивание."
    elif any(user.get("nick", "").lower() == nick.lower() for user in existing_users):
        errors["nick"] = "Пользователь с таким ником уже есть в общем списке."

    if not description:
        errors["description"] = "Добавьте описание пользователя."
    elif len(description) < 10:
        errors["description"] = "Описание должно быть не короче 10 символов."

    if not active_date:
        errors["active_date"] = "Укажите дату последней активности."
    elif not is_valid_activity_date(active_date):
        errors["active_date"] = "Дата должна быть в формате ГГГГ-ММ-ДД и не позже сегодняшнего дня."

    if not phone:
        errors["phone"] = "Укажите телефон."
    elif not is_valid_user_phone(phone):
        errors["phone"] = "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX."

    metric_fields = {
        "events_created": "Укажите количество созданных событий.",
        "comments_count": "Укажите количество комментариев.",
        "notes_count": "Укажите количество заметок.",
        "groups_joined": "Укажите количество групп.",
    }

    for field, message in metric_fields.items():
        if not is_valid_metric(form[field].strip()):
            errors[field] = message

    return errors


# Создает объект существующего пользователя из проверенной формы.
# @param form валидный словарь формы с данными пользователя и метриками.
# @returns словарь пользователя для сохранения в JSON.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note рейтинг не сохраняется вручную, а пересчитывается при загрузке страницы.
def build_active_user(form: dict[str, str]) -> dict[str, str]:
    return {
        "nick": form["nick"].strip(),
        "description": form["description"].strip(),
        "active_date": form["active_date"].strip(),
        "phone": form["phone"].strip(),
        "events_created": parse_metric(form["events_created"]),
        "comments_count": parse_metric(form["comments_count"]),
        "notes_count": parse_metric(form["notes_count"]),
        "groups_joined": parse_metric(form["groups_joined"]),
    }

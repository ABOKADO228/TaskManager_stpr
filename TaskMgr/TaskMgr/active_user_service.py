import json
import re
from datetime import date, datetime
from pathlib import Path


# Формат даты, который отправляет браузерное поле input[type="date"].
DATE_FORMAT = "%Y-%m-%d"

# Минимальный рейтинг, после которого пользователь считается активным.
ACTIVE_SCORE_THRESHOLD = 10

# Регулярное выражение допускает российский телефон с пробелами, скобками и дефисами.
# Точное количество цифр проверяется отдельно.
PHONE_PATTERN = re.compile(r"^\+?[\d\s()\-]{10,20}$")


# Возвращает стандартный путь к JSON-файлу существующих пользователей.
# @returns путь к файлу data/active_users.json.
# @throws не выбрасывает исключения напрямую.
# @note файл хранит всех пользователей с метриками, а не только активных.
def default_active_users_path():
    return Path(__file__).resolve().parent / "data" / "active_users.json"


# Создает пустое состояние формы пользователя с метриками активности.
# @returns словарь с пустыми значениями для текстовых полей и нулями для метрик.
# @throws не выбрасывает исключения.
# @note ключи должны совпадать с name-полями в views/active-users.tpl.
def empty_user_form():
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
def parse_metric(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0

    if number < 0:
        return 0

    return number


# Рассчитывает рейтинг активности пользователя.
# @param user пользователь с метриками events_created, comments_count, notes_count, groups_joined.
# @returns числовой рейтинг активности.
# @throws не выбрасывает исключения.
# @note события и комментарии имеют больший вес, потому что сильнее влияют на работу группы.
def calculate_activity_score(user):
    score = 0
    score += parse_metric(user.get("events_created")) * 4
    score += parse_metric(user.get("comments_count")) * 2
    score += parse_metric(user.get("notes_count"))
    score += parse_metric(user.get("groups_joined")) * 3

    if is_valid_activity_date(str(user.get("active_date", ""))):
        score += 2

    return score


# Добавляет пользователю расчетный рейтинг активности.
# @param user пользователь из JSON-файла.
# @returns копию пользователя с полем activity_score.
# @throws не выбрасывает исключения.
# @note исходный словарь не изменяется, чтобы избежать неожиданных побочных эффектов.
def add_score_to_user(user):
    new_user = dict(user)
    new_user["activity_score"] = calculate_activity_score(user)
    return new_user


# Возвращает пользователя с расчетным рейтингом активности.
# @param user пользователь из JSON-файла.
# @returns копию пользователя с полем activity_score.
# @throws не выбрасывает исключения.
# @note функция оставлена как отдельное имя для совместимости с тестами и другим кодом.
def enrich_user_with_score(user):
    return add_score_to_user(user)


# Загружает всех пользователей из JSON-файла.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns список всех существующих пользователей без фильтрации по активности.
# @throws не выбрасывает исключения наружу; ошибки чтения и JSON обрабатываются внутри.
# @note используется для проверки уникальности и сохранения полного списка.
def load_all_users(path=None):
    users_path = path or default_active_users_path()

    if not users_path.exists():
        return []

    try:
        with users_path.open("r", encoding="utf-8") as file:
            users = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(users, list):
        return []

    return users


# Загружает активных пользователей, выбранных из общего списка по рейтингу.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns список пользователей с activity_score, отсортированный по рейтингу и дате.
# @throws не выбрасывает исключения наружу; ошибки чтения обрабатываются в load_all_users.
# @note активным считается пользователь с рейтингом не ниже ACTIVE_SCORE_THRESHOLD.
def load_active_users(path=None):
    active_users = []

    for user in load_all_users(path):
        user_with_score = add_score_to_user(user)
        if user_with_score["activity_score"] >= ACTIVE_SCORE_THRESHOLD:
            active_users.append(user_with_score)

    return sorted(
        active_users,
        key=lambda user: (user.get("activity_score", 0), user.get("active_date", "")),
        reverse=True,
    )


# Сохраняет общий список существующих пользователей в JSON-файл.
# @param users список всех пользователей для записи.
# @param path путь к JSON-файлу; если None, используется data/active_users.json.
# @returns None.
# @throws OSError если папку или файл не удалось создать/записать.
# @note сохраняется полный список, а активные пользователи вычисляются при чтении.
def save_active_users(users, path=None):
    users_path = path or default_active_users_path()
    users_path.parent.mkdir(parents=True, exist_ok=True)

    with users_path.open("w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)


# Проверяет дату последней активности пользователя.
# @param value строка даты из формы в формате YYYY-MM-DD.
# @returns True, если дата корректна и не позже сегодняшнего дня; иначе False.
# @throws не выбрасывает исключения; ValueError при парсинге даты перехватывается.
# @note будущие даты запрещены, потому что список хранит уже существующую активность.
def is_valid_activity_date(value):
    try:
        active_date = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return False

    return active_date <= date.today()


# Проверяет телефон пользователя.
# @param value телефон, введенный в форму.
# @returns True, если телефон содержит 11 цифр и начинается с 7 или 8; иначе False.
# @throws не выбрасывает исключения.
# @note формат допускает пробелы, скобки и дефисы, но хранится исходная строка.
def is_valid_user_phone(value):
    if not PHONE_PATTERN.match(value):
        return False

    digits = re.sub(r"\D", "", value)

    if len(digits) != 11:
        return False

    return digits[0] == "7" or digits[0] == "8"


# Проверяет, что метрика активности является неотрицательным целым числом.
# @param value значение поля формы.
# @returns True, если значение можно сохранить как число больше или равно нулю.
# @throws не выбрасывает исключения.
# @note пустые значения не принимаются, чтобы рейтинг был однозначным.
def is_valid_metric(value):
    if value == "":
        return False

    try:
        number = int(value)
    except ValueError:
        return False

    return number >= 0


# Проверяет, что описание пользователя похоже на осмысленный текст.
# @param value описание пользователя из формы.
# @returns True, если описание содержит достаточно букв, слов и разных символов.
# @throws не выбрасывает исключения.
# @note защита от строк вроде "1111111111", "----------", "аааааааааа" или "test".
def is_valid_user_description(value):
    text = value.strip()

    if len(text) < 10:
        return False

    letters = re.findall(r"[A-Za-zА-Яа-яЁё]", text)

    if len(letters) < 5:
        return False

    words = re.findall(r"[A-Za-zА-Яа-яЁё]{2,}", text)

    if len(words) < 2:
        return False

    unique_chars = set(text.lower())

    if len(unique_chars) < 5:
        return False

    return True


# Проверяет форму добавления существующего пользователя с метриками активности.
# @param form словарь с полями пользователя и метриками активности.
# @param existing_users уже сохраненные пользователи для проверки уникальности ника.
# @returns словарь ошибок вида {имя_поля: текст_ошибки}; пустой словарь означает успех.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note пользователь попадет в активные только если его расчетный рейтинг пройдет порог.
def validate_active_user(form, existing_users):
    errors = {}

    nick = form["nick"].strip()
    description = form["description"].strip()
    active_date = form["active_date"].strip()
    phone = form["phone"].strip()

    if not nick:
        errors["nick"] = "Введите ник пользователя."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё0-9_.-]{3,24}$", nick):
        errors["nick"] = "Ник должен быть от 3 до 24 символов."
    else:
        for user in existing_users:
            old_nick = user.get("nick", "").lower()
            if old_nick == nick.lower():
                errors["nick"] = "Пользователь с таким ником уже есть."
                break

    if not description:
        errors["description"] = "Введите описание пользователя."
    elif len(description) < 10:
        errors["description"] = "Описание слишком короткое."
    elif not is_valid_user_description(description):
        errors["description"] = "Описание должно быть осмысленным: минимум 2 слова, 5 букв и разные символы."

    if not active_date:
        errors["active_date"] = "Укажите дату последней активности."
    elif not is_valid_activity_date(active_date):
        errors["active_date"] = "Дата должна быть в формате YYYY-MM-DD и не в будущем."

    if not phone:
        errors["phone"] = "Укажите телефон."
    elif not is_valid_user_phone(phone):
        errors["phone"] = "Телефон должен быть похож на +7XXXXXXXXXX или 8XXXXXXXXXX."

    metric_messages = {
        "events_created": "Укажите количество событий.",
        "comments_count": "Укажите количество комментариев.",
        "notes_count": "Укажите количество заметок.",
        "groups_joined": "Укажите количество групп.",
    }

    for field in metric_messages:
        if not is_valid_metric(form[field].strip()):
            errors[field] = metric_messages[field]

    return errors


# Создает объект существующего пользователя из проверенной формы.
# @param form валидный словарь формы с данными пользователя и метриками.
# @returns словарь пользователя для сохранения в JSON.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note рейтинг не сохраняется вручную, а пересчитывается при загрузке страницы.
def build_active_user(form):
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
import json
import re
from datetime import date, datetime
from pathlib import Path


# Формат даты, который отправляет браузерное поле input[type="date"].
DATE_FORMAT = "%Y-%m-%d"

# Регулярное выражение допускает российский телефон с пробелами, скобками и дефисами.
# Точное количество цифр проверяется отдельно.
PHONE_PATTERN = re.compile(r"^\+?[\d\s()\-]{10,20}$")


# Возвращает стандартный путь к JSON-файлу оформленных заказов.
# @returns путь к файлу data/orders.json.
# @throws не выбрасывает исключения напрямую.
# @note путь строится относительно этого файла, а не текущей рабочей папки.
def default_orders_path():
    return Path(__file__).resolve().parent / "data" / "orders.json"


# Создает пустое состояние формы заказа.
# @returns словарь с пустыми значениями для всех полей формы заказа.
# @throws не выбрасывает исключения.
# @note используется при первом открытии страницы и после успешного redirect.
def empty_form():
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
def load_orders(path=None):
    orders_path = path or default_orders_path()

    if not orders_path.exists():
        return []

    try:
        with orders_path.open("r", encoding="utf-8") as file:
            orders = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(orders, list):
        return []

    return sorted(orders, key=lambda order: order.get("date", ""), reverse=True)


# Возвращает только заказы указанного пользователя.
# @param orders полный список заказов из JSON-файла.
# @param user_id идентификатор текущего пользователя из серверной cookie.
# @returns список заказов, у которых owner_id совпадает с user_id.
# @throws не выбрасывает исключения напрямую.
# @note заказы без owner_id считаются старыми общими данными и не показываются в личном кабинете.
def filter_orders_for_user(orders, user_id):
    result = []

    for order in orders:
        if order.get("owner_id") == user_id:
            result.append(order)

    return result


# Загружает личные заказы пользователя из JSON-файла.
# @param user_id идентификатор текущего пользователя.
# @param path путь к JSON-файлу; если None, используется data/orders.json.
# @returns список личных заказов пользователя, отсортированный по дате от новых к старым.
# @throws не выбрасывает исключения наружу; ошибки чтения обрабатываются в load_orders.
def load_orders_for_user(user_id, path=None):
    orders = load_orders(path)
    return filter_orders_for_user(orders, user_id)


# Сохраняет оформленные заказы в JSON-файл.
# @param orders список заказов для записи.
# @param path путь к JSON-файлу; если None, используется data/orders.json.
# @returns None.
# @throws OSError если папку или файл не удалось создать/записать.
# @note ensure_ascii=False нужен, чтобы русские строки оставались читаемыми.
def save_orders(orders, path=None):
    orders_path = path or default_orders_path()
    orders_path.parent.mkdir(parents=True, exist_ok=True)

    with orders_path.open("w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=2)


# Проверяет дату оформления заказа.
# @param value строка даты из формы в формате YYYY-MM-DD.
# @returns True, если дата корректна и не позже сегодняшнего дня; иначе False.
# @throws не выбрасывает исключения; ValueError при парсинге даты перехватывается.
# @note будущие даты запрещены, потому что список хранит уже оформленные заказы.
def is_valid_order_date(value):
    try:
        order_date = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return False

    return order_date <= date.today()


# Проверяет телефон заказа.
# @param value телефон, введенный в форму заказа.
# @returns True, если телефон содержит 11 цифр и начинается с 7 или 8; иначе False.
# @throws не выбрасывает исключения.
# @note формат допускает пробелы, скобки и дефисы, но хранится исходная строка.
def is_valid_phone(value):
    if not PHONE_PATTERN.match(value):
        return False

    digits = re.sub(r"\D", "", value)

    if len(digits) != 11:
        return False

    return digits[0] == "7" or digits[0] == "8"


# Проверяет форму добавления оформленного заказа.
# @param form словарь с полями number, author, text, date, phone.
# @param existing_orders уже сохраненные заказы текущего пользователя для проверки уникальности номера.
# @returns словарь ошибок вида {имя_поля: текст_ошибки}; пустой словарь означает успех.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note имена ключей ошибок совпадают с именами HTML-полей для вывода рядом с input.
def validate_order(form, existing_orders):
    errors = {}

    number = form["number"].strip()
    author = form["author"].strip()
    text = form["text"].strip()
    order_date = form["date"].strip()
    phone = form["phone"].strip()

    if not number:
        errors["number"] = "Введите номер заказа."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё0-9\-]{3,20}$", number):
        errors["number"] = "Номер должен быть от 3 до 20 символов."
    else:
        for order in existing_orders:
            old_number = order.get("number", "").lower()
            if old_number == number.lower():
                errors["number"] = "Заказ с таким номером уже есть."
                break

    if not author:
        errors["author"] = "Введите автора или клиента."
    elif len(author) < 2:
        errors["author"] = "Имя слишком короткое."

    if not text:
        errors["text"] = "Введите описание заказа."
    elif len(text) < 10:
        errors["text"] = "Описание слишком короткое."

    if not order_date:
        errors["date"] = "Укажите дату заказа."
    elif not is_valid_order_date(order_date):
        errors["date"] = "Дата должна быть в формате YYYY-MM-DD и не в будущем."

    if not phone:
        errors["phone"] = "Укажите телефон."
    elif not is_valid_phone(phone):
        errors["phone"] = "Телефон должен быть похож на +7XXXXXXXXXX или 8XXXXXXXXXX."

    return errors


# Создает объект заказа из проверенной формы и привязывает его к владельцу.
# @param form валидный словарь формы с полями number, author, text, date, phone.
# @param owner текущий пользователь с полями id и display_name; если None, owner_id останется пустым.
# @returns словарь заказа для сохранения в JSON.
# @throws KeyError если в form отсутствует обязательный ключ.
# @note функцию нужно вызывать только после validate_order, иначе в JSON могут попасть непроверенные данные.
def build_order(form, owner=None):
    if owner is None:
        owner = {}

    return {
        "number": form["number"].strip(),
        "author": form["author"].strip(),
        "text": form["text"].strip(),
        "date": form["date"].strip(),
        "phone": form["phone"].strip(),
        "owner_id": owner.get("id", ""),
        "owner_name": owner.get("display_name", ""),
    }

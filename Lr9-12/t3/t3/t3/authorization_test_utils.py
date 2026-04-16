import re

EMAIL_PATTERN = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
LOGIN_PATTERN = r'^[A-Za-z]{2,50}$'


def validate_email(mail: str) -> bool:
    return bool(re.fullmatch(EMAIL_PATTERN, mail.strip()))


def validate_login(name: str) -> bool:
    return bool(re.fullmatch(LOGIN_PATTERN, name.strip()))


def is_valid_question(quest: str) -> bool:
    quest = quest.strip()

    if len(quest) <= 3:
        return False
    if quest.isdigit():
        return False

    return True
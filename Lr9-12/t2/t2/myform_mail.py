import re

EMAIL_PATTERN = re.compile(
    r"^(?!.*\.\.)"
    r"[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9])?"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}$"
)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email))
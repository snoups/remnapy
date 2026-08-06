import random
import string
from datetime import datetime, timedelta


def generate_random_string(length: int = 8, chars: str = string.ascii_letters) -> str:
    return "".join(random.choices(chars, k=length))


def generate_password(length: int) -> str:
    return generate_random_string(
        length=length, chars=string.ascii_letters + string.digits
    )


def generate_email(length: int, chars: str = string.ascii_letters) -> str:
    return generate_random_string(length=length, chars=chars) + "@mail.com"


def generate_date_range() -> tuple[str, str]:
    """Generate date range in YYYY-MM-DD format for the past 7 days"""
    end = datetime.now()
    start = end - timedelta(days=7)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')
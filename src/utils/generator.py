import datetime
import random
import string
import uuid


async def generate_password():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


async def generate_token(length=32, prefix="", suffix=""):
    return f"{prefix}{''.join(random.choices(string.ascii_letters + string.digits, k=length))}{suffix}"


async def generate_username(first_name, last_name):
    return f"{first_name.lower()}_{last_name.lower()}"


async def generate_filename(extension="jpg") -> str:
    return (
        f"{datetime.datetime.now().strftime('%Y/%m/%d')}/{uuid.uuid4().hex}.{extension}"
    )

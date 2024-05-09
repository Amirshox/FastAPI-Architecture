from datetime import datetime


def parse_datetime(value):
    if isinstance(value, list):
        return [parse_datetime(v) for v in value]
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None

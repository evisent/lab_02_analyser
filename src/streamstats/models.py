from datetime import datetime

from .errors import InvalidDateError, InvalidEventError

LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def validate_time(text):
    try:
        return datetime.fromisoformat(text)
    except (ValueError, TypeError):
        raise InvalidDateError("invalid timestamp: " + str(text))


def validate_event(row):
    if "timestamp" not in row:
        raise InvalidEventError("the field 'timestamp' is missing")
    if "level" not in row:
        raise InvalidEventError("the field 'level' is missing")
    if "source" not in row:
        raise InvalidEventError("the field 'source' is missing")
    if "message" not in row:
        raise InvalidEventError("the field 'message' is missing")

    level = row["level"]
    if level not in LEVELS:
        raise InvalidEventError("invalid level: " + str(level))

    source = row["source"]
    if not isinstance(source, str) or source == "":
        raise InvalidEventError("invalid source")

    message = row["message"]
    if not isinstance(message, str):
        raise InvalidEventError("invalid message")

    return {
        "timestamp": validate_time(row["timestamp"]),
        "level": level,
        "source": source,
        "message": message,
    }
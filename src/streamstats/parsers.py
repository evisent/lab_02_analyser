import csv
import json

from .errors import InvalidDateError, InvalidEventError, UnsupportedFormatError
from .models import validate_event


def parse_csv(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                event = validate_event(row)
            except (InvalidEventError, InvalidDateError) as e:
                yield (None, str(e))
                continue
            yield (event, None)


def parse_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                yield (None, "bad json: " + line)
                continue
            try:
                event = validate_event(row)
            except (InvalidEventError, InvalidDateError) as e:
                yield (None, str(e))
                continue
            yield (event, None)


PARSERS = {
    "csv": parse_csv,
    "jsonl": parse_jsonl,
}


def get_parser(fmt):
    if fmt not in PARSERS:
        raise UnsupportedFormatError("unknown format: " + fmt)
    return PARSERS[fmt]
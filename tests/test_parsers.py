import pytest

from streamstats.errors import InvalidEventError, UnsupportedFormatError
from streamstats.parsers import get_parser, parse_csv, parse_jsonl


def write_file(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_csv_ok(tmp_path):
    path = write_file(
        tmp_path,
        "1.csv",
        "timestamp,level,source,message\n"
        "2024-05-01T12:30:00,INFO,app,hi\n",
    )
    events = list(parse_csv(path))
    assert len(events) == 1
    assert events[0][0]["level"] == "INFO"
    assert events[0][1] is None


def test_jsonl_ok(tmp_path):
    path = write_file(
        tmp_path,
        "1.jsonl",
        '{"timestamp":"2024-05-01T12:30:00","level":"ERROR","source":"db","message":"oops"}\n',
    )
    events = list(parse_jsonl(path))
    assert len(events) == 1
    assert events[0][0]["level"] == "ERROR"
    assert events[0][1] is None


def test_csv_empty(tmp_path):
    path = write_file(tmp_path, "1.csv", "timestamp,level,source,message\n")
    events = list(parse_csv(path))
    assert events == []


def test_jsonl_bad_line(tmp_path):
    path = write_file(tmp_path, "1.jsonl", "не json\n")
    events = list(parse_jsonl(path))
    assert len(events) == 1
    assert events[0][0] is None
    assert events[0][1] is not None


def test_jsonl_bad_level(tmp_path):
    path = write_file(
        tmp_path,
        "1.jsonl",
        '{"timestamp":"2024-05-01T12:30:00","level":"BANANA","source":"app","message":"x"}\n',
    )
    events = list(parse_jsonl(path))
    assert events[0][0] is None
    assert events[0][1] is not None


def test_jsonl_unicode(tmp_path):
    path = write_file(
        tmp_path,
        "1.jsonl",
        '{"timestamp":"2024-05-01T12:30:00","level":"INFO","source":"приложение","message":"привет"}\n',
    )
    events = list(parse_jsonl(path))
    assert events[0][0]["source"] == "приложение"


def test_bad_format():
    with pytest.raises(UnsupportedFormatError):
        get_parser("xml")
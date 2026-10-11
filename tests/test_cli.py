import json

from streamstats.__main__ import main


def test_cli_ok(tmp_path):
    input = tmp_path / "1.jsonl"
    input.write_text(
        '{"timestamp":"2024-05-01T12:30:00","level":"INFO","source":"app","message":"hi"}\n',
        encoding="utf-8",
    )
    output = tmp_path / "report.json"

    code = main(["analyze", str(input), "--format", "jsonl", "--output", str(output)])

    assert code == 0
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["total"] == 1


def test_cli_bad_returns_2(tmp_path):
    input = tmp_path / "1.jsonl"
    input.write_text("не json\n", encoding="utf-8")
    output = tmp_path / "report.json"

    code = main(["analyze", str(input), "--format", "jsonl", "--output", str(output)])

    assert code == 2


def test_cli_skip_invalid(tmp_path):
    input = tmp_path / "1.jsonl"
    input.write_text(
        "не json\n"
        '{"timestamp":"2024-05-01T12:30:00","level":"INFO","source":"app","message":"hi"}\n',
        encoding="utf-8",
    )
    output = tmp_path / "report.json"

    code = main([
        "analyze", str(input),
        "--format", "jsonl",
        "--output", str(output),
        "--skip-invalid",
    ])

    assert code == 0
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["total"] == 1
    assert data["skipped"] == 1
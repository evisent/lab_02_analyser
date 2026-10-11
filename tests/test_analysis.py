from streamstats.analysis import analyze_files
from streamstats.errors import InvalidEventError


def create_csv(tmp_path, name, lines):
    path = tmp_path / name
    path.write_text(
        "timestamp,level,source,message\n" + "".join(lines),
    )
    return path


def create_jsonl(tmp_path, name, lines):
    path = tmp_path / name
    path.write_text("".join(lines))
    return path


def test_counts(tmp_path):
    path = create_csv(tmp_path, "1.csv", [
        "2024-05-01T12:30:00,INFO,app,hi\n",
        "2024-05-01T12:31:00,ERROR,db,oops\n",
    ])
    report = analyze_files([path], "csv", skip_invalid=False)
    assert report["total"] == 2
    assert report["by_level"] == {"INFO": 1, "ERROR": 1}
    assert report["by_source"] == {"app": 1, "db": 1}


def test_top_error_sources(tmp_path):
    path = create_csv(tmp_path, "1.csv", [
        "2024-05-01T12:30:00,ERROR,db,a\n",
        "2024-05-01T12:31:00,CRITICAL,db,b\n",
        "2024-05-01T12:32:00,ERROR,auth,c\n",
    ])
    report = analyze_files([path], "csv", skip_invalid=False)
    assert report["top_error_sources"] == [("db", 2), ("auth", 1)]

def test_first_last_timestamp(tmp_path):
    path = create_csv(tmp_path, "1.csv", [
        "2024-05-01T12:31:00,INFO,app,x\n",
        "2024-05-01T12:30:00,INFO,app,x\n",
        "2024-05-01T12:34:00,INFO,app,x\n",
    ])
    report = analyze_files([path], "csv", skip_invalid=False)
    assert report["first_timestamp"] == "2024-05-01T12:30:00"
    assert report["last_timestamp"] == "2024-05-01T12:34:00"


def test_empty_file(tmp_path):
    path = create_csv(tmp_path, "1.csv", [])
    report = analyze_files([path], "csv", skip_invalid=False)
    assert report["total"] == 0
    assert report["first_timestamp"] is None
    assert report["last_timestamp"] is None


def test_invalid_raises(tmp_path):
    path = create_csv(tmp_path, "1.csv", [
        "2024-05-01T12:30:00,smth,app,x\n",
    ])
    try:
        analyze_files([path], "csv", skip_invalid=False)
        assert False, "should have broke"
    except InvalidEventError:
        pass


def test_skip_invalid(tmp_path):
    path = create_jsonl(tmp_path, "1.jsonl", [
        "не json\n",
        '{"timestamp":"2024-05-01T12:30:00","level":"INFO","source":"app","message":"ok"}\n',
        '{"timestamp":"2024-05-01T12:31:00","level":"ERROR","source":"db","message":"oops"}\n',
    ])
    report = analyze_files([path], "jsonl", skip_invalid=True)
    assert report["total"] == 2
    assert report["skipped"] == 1
    assert report["by_level"] == {"INFO": 1, "ERROR": 1}


def test_multiple_files(tmp_path):
    file1 = create_csv(tmp_path, "file1.csv", ["2024-05-01T12:30:00,INFO,app,x\n"])
    file2 = create_csv(tmp_path, "file2.csv", ["2024-05-01T12:31:00,ERROR,db,x\n"])
    report = analyze_files([file1, file2], "csv", skip_invalid=False)
    assert report["total"] == 2
    assert report["by_source"] == {"app": 1, "db": 1}
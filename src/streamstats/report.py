import json


def write_report(data, path):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
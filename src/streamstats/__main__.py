import argparse
import sys

from .analysis import analyze_files
from .errors import StreamStatsError
from .report import write_report


def main(argv = None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="streamstats", description="writes a report")
    sub_parser = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub_parser.add_parser("analyze", help="analyzes a file")
    p_analyze.add_argument("inputs", nargs="+")
    p_analyze.add_argument("--format", required=True, choices=["csv", "jsonl"])
    p_analyze.add_argument("--output", required=True)
    p_analyze.add_argument("--skip-invalid", action="store_true")

    args = parser.parse_args(argv)
    try:
        write_report(analyze_files(args.inputs, args.format, args.skip_invalid), args.output)

    except StreamStatsError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import logging

from .errors import InvalidEventError
from .parsers import get_parser

log = logging.getLogger(__name__)


def analyze_files(paths, fmt, skip_invalid):
    parse = get_parser(fmt)

    total = 0
    by_level = {}
    by_source = {}
    error_sources = {}
    first_ts = None
    last_ts = None
    skipped = 0

    for path in paths:
        for event, error in parse(path):
            if error is not None:
                if skip_invalid:
                    skipped += 1
                    log.warning(f"skipped in {path}: {error}")
                    continue
                raise InvalidEventError(error)

            total += 1

            lvl = event["level"]
            if lvl in by_level:
                by_level[lvl] += 1
            else:
                by_level[lvl] = 1

            src = event["source"]
            if src in by_source:
                by_source[src] += 1
            else:
                by_source[src] = 1

            if lvl == "ERROR" or lvl == "CRITICAL":
                if src in error_sources:
                    error_sources[src] += 1
                else:
                    error_sources[src] = 1

            ts = event["timestamp"]
            if first_ts is None or ts < first_ts:
                first_ts = ts
            if last_ts is None or ts > last_ts:
                last_ts = ts

    top = sorted(error_sources.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "total": total,
        "by_level": by_level,
        "by_source": by_source,
        "top_error_sources": top,
        "first_timestamp": first_ts.isoformat() if first_ts else None,
        "last_timestamp": last_ts.isoformat() if last_ts else None,
        "skipped": skipped,
    }
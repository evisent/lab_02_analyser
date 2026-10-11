class StreamStatsError(Exception):
    pass

class InvalidEventError(StreamStatsError):
    pass

class InvalidDateError(StreamStatsError):
    pass

class UnsupportedFormatError(StreamStatsError):
    pass
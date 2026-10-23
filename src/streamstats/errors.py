class ParserError(Exception):
    pass

class InvalidTimestamp(ParserError):
    pass

class InvalidEvent(ParserError):
    pass


class AnalyzeError(Exception):
    pass

class UnsupportedFormat(AnalyzeError):
    pass

class DifferentFormats(AnalyzeError):
    pass

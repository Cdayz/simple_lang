"""Module with useful exceptions for Parser."""


class BadOperationIdentifier(Exception):
    """Bad operation identifier used."""


class BadOperationArgument(Exception):
    """Bad argument provided to operation."""


class BadInPlaceValue(Exception):
    """Bad in-place value provided as argument."""


class PrasingError(Exception):
    """Parsing error."""

    def __init__(self, line_index, line, exception):
        self.line_index = line_index
        self.line_code = line
        self.exception = exception

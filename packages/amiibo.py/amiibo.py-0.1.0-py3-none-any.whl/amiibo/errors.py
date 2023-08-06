class AmiiboException(Exception):
    """Base Exception class"""
    pass

class NotFound(AmiiboException):
    """Raised when Amiibo API Returns 404 code."""
    pass

class ServerDown(AmiiboException):
    """Raised when Amiibo API Returns 500 code."""
    pass

class MissingArgumet(AmiiboException):
    """Raised when no params are given"""
    pass
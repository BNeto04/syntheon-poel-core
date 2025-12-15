class PoelError(Exception):
    """Base exception for Poel."""

    pass


class SechelError(PoelError):
    """Base exception for Sechel client errors."""

    pass


class SechelConnectionError(SechelError):
    """Raised when the Sechel client cannot connect to the server."""

    pass


class SechelAPIError(SechelError):
    """Raised when the Sechel API returns an error."""

    pass

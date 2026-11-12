"""
Domain exceptions.

The core raises these; `app/errors.py` translates them to HTTP responses in a
single exception handler. They do not know anything about HTTP.
"""


class DomainError(Exception):
    """Base of every error the core can raise. `code` is the `ErrorCode` of the contract."""

    code: str = "DOMAIN_ERROR"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def to_detail(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}

class InvalidParameters(DomainError):
    code = "INVALID_PARAMETERS"


class InvalidFile(DomainError):
    code = "INVALID_FILE"

    def __init__(self, message: str = "The file cannot be opened as an image.") -> None:
        super().__init__(message)


class UnsupportedFormat(DomainError):
    code = "UNSUPPORTED_FORMAT"

    def __init__(self, image_format: str | None) -> None:
        super().__init__(f"The format '{image_format}' is not supported. Use PNG, JPEG, WEBP or BMP.")
        self.image_format = image_format

class InvalidCoordinates(DomainError):
    code = "INVALID_COORDINATES"

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> None:
        super().__init__(
            f"The selected point ({x}, {y}) is outside "
            f"the image boundaries ({width}x{height})."
        )
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class FileTooLarge(DomainError):
    code = "FILE_TOO_LARGE"

    def __init__(self, max_bytes: int) -> None:
        super().__init__(f"The file exceeds the maximum size of {max_bytes // (1024 * 1024)} MB.")
        self.max_bytes = max_bytes

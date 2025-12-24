"""Custom exception hierarchy for MRDR."""


class MRDRError(Exception):
    """Base exception for all MRDR errors."""

    pass


class DatabaseError(MRDRError):
    """Database-related errors."""

    pass


class DatabaseNotFoundError(DatabaseError):
    """Database file not found.

    Attributes:
        path: The path where the database was expected.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"Database not found: {path}")


class ValidationError(DatabaseError):
    """Schema validation failed.

    Attributes:
        entry: The entry identifier that failed validation.
        errors: List of validation error messages.
    """

    def __init__(self, entry: str, errors: list[str]) -> None:
        self.entry = entry
        self.errors = errors
        super().__init__(f"Validation failed for {entry}: {errors}")


class QueryError(MRDRError):
    """Query-related errors."""

    pass


class LanguageNotFoundError(QueryError):
    """Requested language not in database.

    Attributes:
        language: The language that was not found.
        suggestions: List of similar language names as suggestions.
    """

    def __init__(self, language: str, suggestions: list[str]) -> None:
        self.language = language
        self.suggestions = suggestions
        suggestion_text = ", ".join(suggestions) if suggestions else "none"
        super().__init__(
            f"Language '{language}' not found. Did you mean: {suggestion_text}?"
        )


class ConfigError(MRDRError):
    """Configuration-related errors."""

    pass

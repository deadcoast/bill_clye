"""Validation error collection for MRDR database loaders.

This module provides a standardized way to collect and report validation
errors across all database loaders. It supports collecting errors with
entry identifiers and specific field failures.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class ValidationSeverity(str, Enum):
    """Severity level for validation errors."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationError:
    """A single validation error.

    Attributes:
        entry_id: Identifier of the entry that failed validation.
        field: The field that failed validation (if applicable).
        message: Human-readable error message.
        severity: Severity level of the error.
        details: Additional error details.
    """

    entry_id: str
    field: str | None
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "entry_id": self.entry_id,
            "message": self.message,
            "severity": self.severity.value,
        }
        if self.field:
            result["field"] = self.field
        if self.details:
            result["details"] = self.details
        return result


@dataclass
class ValidationResult:
    """Result of validating a database.

    Attributes:
        database_type: Type of database validated.
        database_path: Path to the database file.
        total_entries: Total number of entries processed.
        valid_entries: Number of valid entries.
        errors: List of validation errors.
    """

    database_type: str
    database_path: Path
    total_entries: int = 0
    valid_entries: int = 0
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if validation passed with no errors."""
        return len([e for e in self.errors if e.severity == ValidationSeverity.ERROR]) == 0

    @property
    def error_count(self) -> int:
        """Get count of errors (excluding warnings)."""
        return len([e for e in self.errors if e.severity == ValidationSeverity.ERROR])

    @property
    def warning_count(self) -> int:
        """Get count of warnings."""
        return len([e for e in self.errors if e.severity == ValidationSeverity.WARNING])

    def add_error(
        self,
        entry_id: str,
        message: str,
        field: str | None = None,
        severity: ValidationSeverity = ValidationSeverity.ERROR,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Add a validation error.

        Args:
            entry_id: Identifier of the entry that failed.
            message: Error message.
            field: Field that failed validation.
            severity: Error severity level.
            details: Additional error details.
        """
        self.errors.append(
            ValidationError(
                entry_id=entry_id,
                field=field,
                message=message,
                severity=severity,
                details=details or {},
            )
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "database_type": self.database_type,
            "database_path": str(self.database_path),
            "total_entries": self.total_entries,
            "valid_entries": self.valid_entries,
            "is_valid": self.is_valid,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "errors": [e.to_dict() for e in self.errors],
        }


class ValidationCollector:
    """Collects validation results from multiple databases.

    Provides a centralized way to aggregate validation results
    from all database loaders.
    """

    def __init__(self) -> None:
        """Initialize the validation collector."""
        self._results: list[ValidationResult] = []

    @property
    def results(self) -> list[ValidationResult]:
        """Get all validation results."""
        return self._results

    def add_result(self, result: ValidationResult) -> None:
        """Add a validation result.

        Args:
            result: The validation result to add.
        """
        self._results.append(result)

    def get_result(self, database_type: str) -> ValidationResult | None:
        """Get validation result for a specific database type.

        Args:
            database_type: The database type to look up.

        Returns:
            The ValidationResult if found, None otherwise.
        """
        for result in self._results:
            if result.database_type == database_type:
                return result
        return None

    @property
    def all_valid(self) -> bool:
        """Check if all databases passed validation."""
        return all(r.is_valid for r in self._results)

    @property
    def total_errors(self) -> int:
        """Get total error count across all databases."""
        return sum(r.error_count for r in self._results)

    @property
    def total_warnings(self) -> int:
        """Get total warning count across all databases."""
        return sum(r.warning_count for r in self._results)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "all_valid": self.all_valid,
            "total_errors": self.total_errors,
            "total_warnings": self.total_warnings,
            "databases": [r.to_dict() for r in self._results],
        }

    def clear(self) -> None:
        """Clear all collected results."""
        self._results = []

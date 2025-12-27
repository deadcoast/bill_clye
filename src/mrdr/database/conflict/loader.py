"""Conflict loader for MRDR.

This module handles loading and managing syntax conflict definitions
from the database/conflicts/ directory.
"""

import json
import logging
from pathlib import Path

from pydantic import ValidationError

from mrdr.database.conflict.schema import (
    ConflictDatabase,
    ConflictEntry,
)
from mrdr.database.validation import ValidationResult, ValidationSeverity

logger = logging.getLogger(__name__)

DEFAULT_CONFLICT_PATH = Path("database/conflicts/conflict_database.json")


class ConflictNotFoundError(Exception):
    """Conflict not found.

    Attributes:
        conflict_id: The conflict ID that was not found.
        available: List of available conflict IDs.
    """

    def __init__(self, conflict_id: str, available: list[str]) -> None:
        self.conflict_id = conflict_id
        self.available = available
        available_text = ", ".join(available) if available else "none"
        super().__init__(f"Conflict '{conflict_id}' not found. Available: {available_text}")


class ConflictLoader:
    """Loads and manages syntax conflict definitions.

    Provides access to syntax conflicts between programming languages
    that share the same docstring delimiters.
    """

    def __init__(self, database_path: Path | str | None = None) -> None:
        """Initialize the conflict loader.

        Args:
            database_path: Path to the conflict JSON database file.
                          Defaults to database/conflicts/conflict_database.json
        """
        self._path = Path(database_path) if database_path else DEFAULT_CONFLICT_PATH
        self._database: ConflictDatabase | None = None
        self._conflicts_by_id: dict[str, ConflictEntry] = {}
        self._conflicts_by_language: dict[str, list[ConflictEntry]] = {}
        self._loaded = False
        self._validation_result: ValidationResult | None = None

    @property
    def path(self) -> Path:
        """Get the conflict database path."""
        return self._path

    @property
    def validation_result(self) -> ValidationResult | None:
        """Get the detailed validation result from the last load operation."""
        return self._validation_result

    def load(self) -> ConflictDatabase:
        """Load the conflict database.

        Returns:
            The loaded ConflictDatabase.

        Raises:
            FileNotFoundError: If the database file doesn't exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        self._conflicts_by_id = {}
        self._conflicts_by_language = {}

        if not self._path.exists():
            logger.warning("Conflict database not found: %s", self._path)
            raise FileNotFoundError(f"Conflict database not found: {self._path}")

        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)

        # Count total entries before validation
        total_entries = len(data.get("conflicts", []))

        # Initialize validation result
        self._validation_result = ValidationResult(
            database_type="conflicts",
            database_path=self._path,
            total_entries=total_entries,
        )

        try:
            self._database = ConflictDatabase.model_validate(data)
        except ValidationError as e:
            for err in e.errors():
                field_path = ".".join(str(loc) for loc in err.get("loc", []))
                self._validation_result.add_error(
                    entry_id="database",
                    message=err.get("msg", "Validation failed"),
                    field=field_path if field_path else None,
                    severity=ValidationSeverity.ERROR,
                    details={"type": err.get("type", "unknown")},
                )
            raise

        # Build lookup indexes
        for conflict in self._database.conflicts:
            self._conflicts_by_id[conflict.id.upper()] = conflict

            # Index by language
            for language in conflict.languages:
                lang_lower = language.lower()
                if lang_lower not in self._conflicts_by_language:
                    self._conflicts_by_language[lang_lower] = []
                self._conflicts_by_language[lang_lower].append(conflict)

        self._validation_result.valid_entries = len(self._conflicts_by_id)
        self._loaded = True
        return self._database

    def get_conflict(self, conflict_id: str) -> ConflictEntry:
        """Get a conflict by ID.

        Args:
            conflict_id: The conflict ID (case-insensitive).

        Returns:
            The ConflictEntry if found.

        Raises:
            ConflictNotFoundError: If the conflict is not found.
        """
        if not self._loaded:
            self.load()

        conflict_id_upper = conflict_id.upper()
        if conflict_id_upper in self._conflicts_by_id:
            return self._conflicts_by_id[conflict_id_upper]

        raise ConflictNotFoundError(conflict_id, self.list_conflicts())

    def get_conflict_for_language(self, language: str) -> list[ConflictEntry]:
        """Get all conflicts involving a specific language.

        Args:
            language: The language name (case-insensitive).

        Returns:
            List of conflicts involving the language.
        """
        if not self._loaded:
            self.load()

        lang_lower = language.lower()
        return self._conflicts_by_language.get(lang_lower, [])

    def list_conflicts(self) -> list[str]:
        """Get all available conflict IDs.

        Returns:
            Sorted list of all conflict IDs.
        """
        if not self._loaded:
            self.load()

        return sorted(self._conflicts_by_id.keys())

    def list_languages(self) -> list[str]:
        """Get all languages with documented conflicts.

        Returns:
            Sorted list of language names.
        """
        if not self._loaded:
            self.load()

        return sorted(self._conflicts_by_language.keys())

    def get_all(self) -> list[ConflictEntry]:
        """Get all conflict entries.

        Returns:
            List of all ConflictEntry objects.
        """
        if not self._loaded:
            self.load()

        return list(self._conflicts_by_id.values())

    def search(self, query: str) -> list[ConflictEntry]:
        """Search conflicts by ID, delimiter, or language.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching ConflictEntry objects.
        """
        if not self._loaded:
            self.load()

        query_lower = query.lower()
        results = []

        for conflict in self._conflicts_by_id.values():
            if (
                query_lower in conflict.id.lower()
                or query_lower in conflict.delimiter.lower()
                or query_lower in conflict.resolution.lower()
                or any(query_lower in lang.lower() for lang in conflict.languages)
            ):
                results.append(conflict)

        return results

    def get_conflicts_for_delimiter(self, delimiter: str) -> list[ConflictEntry]:
        """Get all conflicts for a specific delimiter.

        Args:
            delimiter: The delimiter string.

        Returns:
            List of conflicts for the delimiter.
        """
        if not self._loaded:
            self.load()

        return [
            conflict
            for conflict in self._conflicts_by_id.values()
            if conflict.delimiter == delimiter
        ]

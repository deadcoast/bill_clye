"""Database loader for MRDR.

This module handles loading and validating docstring entries from
the JSON database file.
"""

import json
import logging
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from mrdr.database.base import DataSource
from mrdr.database.schema import DocstringEntry

logger = logging.getLogger(__name__)

DEFAULT_DATABASE_PATH = Path("database/docstrings/docstring_database.json")


class DatabaseLoader(DataSource):
    """Loads and validates docstring entries from JSON database.

    Implements the DataSource protocol for accessing the docstring database.
    Invalid entries are logged and skipped during loading.
    """

    def __init__(self, database_path: Path | str | None = None) -> None:
        """Initialize the database loader.

        Args:
            database_path: Path to the database JSON file.
                          Defaults to database/docstrings/docstring_database.json
        """
        self._path = Path(database_path) if database_path else DEFAULT_DATABASE_PATH
        self._entries: list[DocstringEntry] = []
        self._raw_data: dict[str, Any] = {}
        self._loaded = False
        self._validation_errors: list[tuple[str, list[str]]] = []

    @property
    def path(self) -> Path:
        """Get the database file path."""
        return self._path

    @property
    def validation_errors(self) -> list[tuple[str, list[str]]]:
        """Get validation errors from the last load operation."""
        return self._validation_errors

    def load(self) -> list[dict[str, Any]]:
        """Load all entries from the database file.

        Returns:
            A list of all valid entries as dictionaries.

        Raises:
            FileNotFoundError: If the database file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        if not self._path.exists():
            raise FileNotFoundError(f"Database not found: {self._path}")

        with open(self._path, encoding="utf-8") as f:
            self._raw_data = json.load(f)

        self._entries = []
        self._validation_errors = []

        raw_entries = self._raw_data.get("entries", [])
        for entry_data in raw_entries:
            try:
                entry = DocstringEntry(**entry_data)
                self._entries.append(entry)
            except ValidationError as e:
                language = entry_data.get("language", "unknown")
                errors = [str(err) for err in e.errors()]
                self._validation_errors.append((language, errors))
                logger.warning(
                    "Validation failed for entry '%s': %s",
                    language,
                    errors,
                )

        self._loaded = True
        return [entry.model_dump() for entry in self._entries]

    def query(self, **filters: Any) -> list[dict[str, Any]]:
        """Query entries with filters.

        Args:
            **filters: Key-value pairs to filter entries.
                      Supports 'language' filter for exact match.

        Returns:
            A list of matching entries as dictionaries.
        """
        if not self._loaded:
            self.load()

        results = self._entries

        if "language" in filters:
            lang = filters["language"]
            results = [e for e in results if e.language.lower() == lang.lower()]

        return [entry.model_dump() for entry in results]

    def get_entries(self) -> list[DocstringEntry]:
        """Get all valid entries as DocstringEntry objects.

        Returns:
            A list of validated DocstringEntry objects.
        """
        if not self._loaded:
            self.load()
        return self._entries

    def get_entry(self, language: str) -> DocstringEntry | None:
        """Get a single entry by language name.

        Args:
            language: The programming language name (case-insensitive).

        Returns:
            The DocstringEntry if found, None otherwise.
        """
        if not self._loaded:
            self.load()

        for entry in self._entries:
            if entry.language.lower() == language.lower():
                return entry
        return None

    def get_languages(self) -> list[str]:
        """Get all language names in the database.

        Returns:
            A list of language names.
        """
        if not self._loaded:
            self.load()
        return [entry.language for entry in self._entries]

    def get_metadata(self) -> dict[str, Any]:
        """Get database metadata (manifest info).

        Returns:
            Dictionary with manifest_name, version, schema_origin.
        """
        if not self._loaded:
            self.load()
        return {
            "manifest_name": self._raw_data.get("manifest_name"),
            "version": self._raw_data.get("version"),
            "schema_origin": self._raw_data.get("schema_origin"),
        }

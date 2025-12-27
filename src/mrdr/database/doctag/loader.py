"""Doctag loader for MRDR.

This module provides access to doctag definitions from the database.
Supports loading from both the JSON database file and the legacy
in-memory database.
"""

import json
import logging
from pathlib import Path

from mrdr.database.doctag.schema import (
    DOCTAG_DATABASE,
    DoctagCategory,
    DoctagDatabase,
    DoctagDefinition,
    DoctagEntry,
)

logger = logging.getLogger(__name__)

DEFAULT_DOCTAG_PATH = Path("database/doctags/doctag_database.json")


class DoctagNotFoundError(Exception):
    """Raised when a doctag is not found in the database."""

    def __init__(self, tag_id: str, available: list[str]) -> None:
        """Initialize the error.

        Args:
            tag_id: The requested tag ID that was not found.
            available: List of available tag IDs.
        """
        self.tag_id = tag_id
        self.available = available
        super().__init__(f"Doctag '{tag_id}' not found")


class DoctagLoader:
    """Loader for doctag definitions.

    Provides access to the doctag database with query and lookup methods.
    Supports loading from JSON file or using the legacy in-memory database.
    """

    def __init__(self, database_path: Path | str | None = None) -> None:
        """Initialize the doctag loader.

        Args:
            database_path: Path to the doctag JSON database file.
                          Defaults to database/doctags/doctag_database.json
        """
        self._path = Path(database_path) if database_path else DEFAULT_DOCTAG_PATH
        self._entries: dict[str, DoctagEntry] = {}
        self._legacy_database = DOCTAG_DATABASE
        self._loaded = False
        self._use_json = True

    def load(self) -> list[DoctagEntry]:
        """Load all doctag entries from the JSON database.

        Returns:
            List of all DoctagEntry objects.
        """
        self._entries = {}

        if not self._path.exists():
            logger.warning("Doctag database not found: %s, using legacy", self._path)
            self._use_json = False
            self._loaded = True
            return self._load_from_legacy()

        try:
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)

            db = DoctagDatabase.model_validate(data)
            for entry in db.doctags:
                self._entries[entry.id.upper()] = entry

            self._loaded = True
            return list(self._entries.values())

        except (json.JSONDecodeError, Exception) as e:
            logger.warning("Failed to load doctag database: %s, using legacy", e)
            self._use_json = False
            self._loaded = True
            return self._load_from_legacy()

    def _load_from_legacy(self) -> list[DoctagEntry]:
        """Load entries from the legacy in-memory database.

        Returns:
            List of DoctagEntry objects converted from legacy definitions.
        """
        entries = []
        for tag_id, defn in self._legacy_database.items():
            entry = DoctagEntry(
                id=defn.id,
                symbol=defn.symbol,
                short_name=defn.short_name,
                description=defn.description,
                category=defn.category,
                example=defn.example,
            )
            self._entries[tag_id.upper()] = entry
            entries.append(entry)
        return entries

    def get(self, tag_id: str) -> DoctagEntry | DoctagDefinition:
        """Get a doctag by ID.

        Args:
            tag_id: The tag identifier (e.g., "DDL01", "GRM05").

        Returns:
            The DoctagEntry or DoctagDefinition for the requested tag.

        Raises:
            DoctagNotFoundError: If the tag ID is not found.
        """
        if not self._loaded:
            self.load()

        tag_id_upper = tag_id.upper()

        # Try JSON entries first
        if tag_id_upper in self._entries:
            return self._entries[tag_id_upper]

        # Fall back to legacy database
        if tag_id_upper in self._legacy_database:
            return self._legacy_database[tag_id_upper]

        raise DoctagNotFoundError(tag_id, self.list_ids())

    def list_ids(self) -> list[str]:
        """Get all available tag IDs.

        Returns:
            List of all tag IDs in the database.
        """
        if not self._loaded:
            self.load()

        if self._entries:
            return sorted(self._entries.keys())
        return sorted(self._legacy_database.keys())

    def list_by_category(self, category: DoctagCategory | str) -> list[DoctagEntry]:
        """Get all doctags in a specific category.

        Args:
            category: The category to filter by (DoctagCategory enum or string).

        Returns:
            List of DoctagEntry objects in the category.
        """
        if not self._loaded:
            self.load()

        # Normalize category to string value
        if isinstance(category, DoctagCategory):
            cat_value = category.value
        else:
            cat_value = category.upper()

        results = []

        # Search JSON entries
        for entry in self._entries.values():
            if entry.category.value == cat_value:
                results.append(entry)

        # If no JSON entries, search legacy
        if not results and not self._entries:
            for defn in self._legacy_database.values():
                if defn.category.value == cat_value:
                    entry = DoctagEntry(
                        id=defn.id,
                        symbol=defn.symbol,
                        short_name=defn.short_name,
                        description=defn.description,
                        category=defn.category,
                        example=defn.example,
                    )
                    results.append(entry)

        return results

    def search(self, query: str) -> list[DoctagEntry]:
        """Search doctags by ID, symbol, or short name.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching DoctagEntry objects.
        """
        if not self._loaded:
            self.load()

        query_lower = query.lower()
        results = []

        # Search JSON entries
        for entry in self._entries.values():
            if (
                query_lower in entry.id.lower()
                or query_lower in entry.symbol.lower()
                or query_lower in entry.short_name.lower()
                or query_lower in entry.description.lower()
            ):
                results.append(entry)

        # If no JSON entries, search legacy
        if not results and not self._entries:
            for defn in self._legacy_database.values():
                if (
                    query_lower in defn.id.lower()
                    or query_lower in defn.symbol.lower()
                    or query_lower in defn.short_name.lower()
                    or query_lower in defn.description.lower()
                ):
                    entry = DoctagEntry(
                        id=defn.id,
                        symbol=defn.symbol,
                        short_name=defn.short_name,
                        description=defn.description,
                        category=defn.category,
                        example=defn.example,
                    )
                    results.append(entry)

        return results

    def get_all(self) -> list[DoctagEntry]:
        """Get all doctag definitions.

        Returns:
            List of all DoctagEntry objects.
        """
        if not self._loaded:
            self.load()

        if self._entries:
            return list(self._entries.values())

        # Convert legacy to entries
        return [
            DoctagEntry(
                id=defn.id,
                symbol=defn.symbol,
                short_name=defn.short_name,
                description=defn.description,
                category=defn.category,
                example=defn.example,
            )
            for defn in self._legacy_database.values()
        ]

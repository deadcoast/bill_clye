"""Dictionary loader for MRDR.

This module handles loading and managing dictionary definitions from
the database/dictionary/ directory.
"""

import json
import logging
from pathlib import Path

from mrdr.database.dictionary.schema import (
    DictionaryDatabase,
    DictionaryEntry,
    HierarchyLevel,
)

logger = logging.getLogger(__name__)

DEFAULT_DICTIONARY_PATH = Path("database/dictionary/dictionary_database.json")


class DictionaryNotFoundError(Exception):
    """Dictionary term not found.

    Attributes:
        term: The term that was not found.
        available: List of available terms.
    """

    def __init__(self, term: str, available: list[str]) -> None:
        self.term = term
        self.available = available
        available_text = ", ".join(available[:10]) if available else "none"
        if len(available) > 10:
            available_text += f"... ({len(available)} total)"
        super().__init__(f"Term '{term}' not found. Available: {available_text}")


class DictionaryLoader:
    """Loads and manages dictionary definitions from the database.

    Provides access to the MRDR dictionary hierarchy with methods
    for term lookup, hierarchy traversal, and filtering by level.
    """

    def __init__(self, database_path: Path | str | None = None) -> None:
        """Initialize the dictionary loader.

        Args:
            database_path: Path to the dictionary JSON database file.
                          Defaults to database/dictionary/dictionary_database.json
        """
        self._path = Path(database_path) if database_path else DEFAULT_DICTIONARY_PATH
        self._database: DictionaryDatabase | None = None
        self._entries_by_name: dict[str, DictionaryEntry] = {}
        self._entries_by_alias: dict[str, DictionaryEntry] = {}
        self._loaded = False

    @property
    def path(self) -> Path:
        """Get the dictionary database path."""
        return self._path

    def load(self) -> DictionaryDatabase:
        """Load the complete dictionary database.

        Returns:
            The loaded DictionaryDatabase.

        Raises:
            FileNotFoundError: If the database file doesn't exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        self._entries_by_name = {}
        self._entries_by_alias = {}

        if not self._path.exists():
            logger.warning("Dictionary database not found: %s", self._path)
            raise FileNotFoundError(f"Dictionary database not found: {self._path}")

        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)

        self._database = DictionaryDatabase.model_validate(data)

        # Build lookup indexes
        for entry in self._database.get_all_entries():
            self._entries_by_name[entry.name.upper()] = entry
            self._entries_by_alias[entry.alias.lower()] = entry

        self._loaded = True
        return self._database

    def get_term(self, name: str) -> DictionaryEntry:
        """Get a term by name or alias.

        Args:
            name: The term name (case-insensitive) or alias.

        Returns:
            The DictionaryEntry if found.

        Raises:
            DictionaryNotFoundError: If the term is not found.
        """
        if not self._loaded:
            self.load()

        # Try exact name match (uppercase)
        name_upper = name.upper()
        if name_upper in self._entries_by_name:
            return self._entries_by_name[name_upper]

        # Try alias match (lowercase)
        name_lower = name.lower()
        if name_lower in self._entries_by_alias:
            return self._entries_by_alias[name_lower]

        raise DictionaryNotFoundError(name, self.list_terms())

    def get_hierarchy_path(self, name: str) -> list[DictionaryEntry]:
        """Get the path from root to the specified term.

        Traverses the hierarchy from the term up to its ancestors.

        Args:
            name: The term name or alias.

        Returns:
            List of DictionaryEntry objects from root to the term.
            The list is ordered from highest level (grandparent) to lowest.

        Raises:
            DictionaryNotFoundError: If the term is not found.
        """
        if not self._loaded:
            self.load()

        entry = self.get_term(name)
        path = [entry]

        # Build path based on hierarchy level
        level_order = [
            HierarchyLevel.GRANDCHILD,
            HierarchyLevel.CHILD,
            HierarchyLevel.PARENT,
            HierarchyLevel.GRANDPARENT,
            HierarchyLevel.NAMETYPE,
        ]

        current_level_idx = level_order.index(entry.level) if entry.level in level_order else -1

        # Walk up the hierarchy
        if current_level_idx >= 0:
            for i in range(current_level_idx + 1, len(level_order)):
                parent_level = level_order[i]
                parent_entries = self.get_entries_by_level(parent_level)
                if parent_entries:
                    # Find a parent that contains this entry as a child
                    for parent in parent_entries:
                        if entry.name in parent.children or not parent.children:
                            path.insert(0, parent)
                            break

        return path

    def get_entries_by_level(self, level: HierarchyLevel | str) -> list[DictionaryEntry]:
        """Get all entries at a specific hierarchy level.

        Args:
            level: The hierarchy level (HierarchyLevel enum or string).

        Returns:
            List of DictionaryEntry objects at the specified level.
        """
        if not self._loaded:
            self.load()

        if self._database is None:
            return []

        # Normalize level to enum
        if isinstance(level, str):
            try:
                level = HierarchyLevel(level.lower())
            except ValueError:
                return []

        return self._database.get_entries_by_level(level)

    def list_terms(self) -> list[str]:
        """Get all available term names.

        Returns:
            Sorted list of all term names.
        """
        if not self._loaded:
            self.load()

        return sorted(self._entries_by_name.keys())

    def list_aliases(self) -> list[str]:
        """Get all available term aliases.

        Returns:
            Sorted list of all term aliases.
        """
        if not self._loaded:
            self.load()

        return sorted(self._entries_by_alias.keys())

    def search(self, query: str) -> list[DictionaryEntry]:
        """Search terms by name, alias, or description.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching DictionaryEntry objects.
        """
        if not self._loaded:
            self.load()

        query_lower = query.lower()
        results = []

        for entry in self._entries_by_name.values():
            if (
                query_lower in entry.name.lower()
                or query_lower in entry.alias.lower()
                or query_lower in entry.description.lower()
            ):
                results.append(entry)

        return results

    def get_all(self) -> list[DictionaryEntry]:
        """Get all dictionary entries.

        Returns:
            List of all DictionaryEntry objects.
        """
        if not self._loaded:
            self.load()

        return list(self._entries_by_name.values())

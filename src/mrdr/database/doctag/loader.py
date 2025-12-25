"""Doctag loader for MRDR.

This module provides access to doctag definitions from the database.
"""

from mrdr.database.doctag.schema import (
    DOCTAG_DATABASE,
    DoctagCategory,
    DoctagDefinition,
)


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
    """

    def __init__(self) -> None:
        """Initialize the doctag loader."""
        self._database = DOCTAG_DATABASE

    def get(self, tag_id: str) -> DoctagDefinition:
        """Get a doctag by ID.

        Args:
            tag_id: The tag identifier (e.g., "DDL01", "GRM05").

        Returns:
            The DoctagDefinition for the requested tag.

        Raises:
            DoctagNotFoundError: If the tag ID is not found.
        """
        tag_id_upper = tag_id.upper()
        if tag_id_upper not in self._database:
            raise DoctagNotFoundError(tag_id, self.list_ids())
        return self._database[tag_id_upper]

    def list_ids(self) -> list[str]:
        """Get all available tag IDs.

        Returns:
            List of all tag IDs in the database.
        """
        return sorted(self._database.keys())

    def list_by_category(self, category: DoctagCategory) -> list[DoctagDefinition]:
        """Get all doctags in a specific category.

        Args:
            category: The category to filter by.

        Returns:
            List of DoctagDefinition objects in the category.
        """
        return [
            tag for tag in self._database.values()
            if tag.category == category
        ]

    def search(self, query: str) -> list[DoctagDefinition]:
        """Search doctags by ID, symbol, or short name.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching DoctagDefinition objects.
        """
        query_lower = query.lower()
        results = []
        for tag in self._database.values():
            if (
                query_lower in tag.id.lower()
                or query_lower in tag.symbol.lower()
                or query_lower in tag.short_name.lower()
                or query_lower in tag.description.lower()
            ):
                results.append(tag)
        return results

    def get_all(self) -> list[DoctagDefinition]:
        """Get all doctag definitions.

        Returns:
            List of all DoctagDefinition objects.
        """
        return list(self._database.values())

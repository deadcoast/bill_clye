"""Query operations for the MRDR database.

This module provides query functions for searching and retrieving
docstring entries from the database.
"""

import difflib
from typing import Optional

from mrdr.database.loader import DatabaseLoader
from mrdr.database.schema import DocstringEntry


class QueryEngine:
    """Query engine for docstring database operations.

    Provides methods for querying, listing, and searching the database
    with fuzzy matching support for suggestions.
    """

    def __init__(self, loader: DatabaseLoader | None = None) -> None:
        """Initialize the query engine.

        Args:
            loader: DatabaseLoader instance. Creates a new one if not provided.
        """
        self._loader = loader or DatabaseLoader()

    @property
    def loader(self) -> DatabaseLoader:
        """Get the underlying database loader."""
        return self._loader

    def query_by_language(self, language: str) -> Optional[DocstringEntry]:
        """Query docstring syntax for a specific language.

        Args:
            language: The programming language name (case-insensitive).

        Returns:
            The DocstringEntry if found, None otherwise.
        """
        return self._loader.get_entry(language)

    def list_languages(self) -> list[str]:
        """List all supported languages in the database.

        Returns:
            A sorted list of all language names.
        """
        return sorted(self._loader.get_languages())

    def get_suggestions(
        self, query: str, n: int = 3, cutoff: float = 0.5
    ) -> list[str]:
        """Get fuzzy-matched suggestions for a query string.

        Uses difflib.get_close_matches to find similar language names.

        Args:
            query: The search query string.
            n: Maximum number of suggestions to return.
            cutoff: Similarity threshold (0.0 to 1.0).

        Returns:
            A list of suggested language names.
        """
        languages = self._loader.get_languages()
        # Case-insensitive matching
        lower_languages = {lang.lower(): lang for lang in languages}
        matches = difflib.get_close_matches(
            query.lower(),
            lower_languages.keys(),
            n=n,
            cutoff=cutoff,
        )
        return [lower_languages[m] for m in matches]

    def search(self, query: str) -> list[DocstringEntry]:
        """Search for entries matching a query string.

        Searches language names, tags, and metadata for matches.

        Args:
            query: The search query string.

        Returns:
            A list of matching DocstringEntry objects.
        """
        query_lower = query.lower()
        results = []

        for entry in self._loader.get_entries():
            # Match language name
            if query_lower in entry.language.lower():
                results.append(entry)
                continue

            # Match tags
            if any(query_lower in tag.lower() for tag in entry.tags):
                results.append(entry)
                continue

            # Match syntax type
            if query_lower in entry.syntax.type.lower():
                results.append(entry)
                continue

        return results

    def get_by_syntax_type(self, syntax_type: str) -> list[DocstringEntry]:
        """Get all entries with a specific syntax type.

        Args:
            syntax_type: The syntax type to filter by.

        Returns:
            A list of matching DocstringEntry objects.
        """
        return [
            entry
            for entry in self._loader.get_entries()
            if entry.syntax.type.lower() == syntax_type.lower()
        ]

    def get_by_tag(self, tag: str) -> list[DocstringEntry]:
        """Get all entries with a specific tag.

        Args:
            tag: The tag to filter by.

        Returns:
            A list of matching DocstringEntry objects.
        """
        tag_lower = tag.lower()
        return [
            entry
            for entry in self._loader.get_entries()
            if any(t.lower() == tag_lower for t in entry.tags)
        ]

    def get_conflicts(self, language: str) -> list[DocstringEntry]:
        """Get entries that conflict with a given language.

        Args:
            language: The language to find conflicts for.

        Returns:
            A list of conflicting DocstringEntry objects.
        """
        entry = self.query_by_language(language)
        if not entry:
            return []

        conflicts = []
        for other in self._loader.get_entries():
            if other.language == entry.language:
                continue
            # Check if conflict_ref mentions this language
            if other.conflict_ref and language.lower() in other.conflict_ref.lower():
                conflicts.append(other)
            # Check if this entry's conflict_ref mentions the other
            if entry.conflict_ref and other.language.lower() in entry.conflict_ref.lower():
                conflicts.append(other)

        return conflicts

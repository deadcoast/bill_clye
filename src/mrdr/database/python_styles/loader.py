"""Python styles loader for MRDR.

This module handles loading and managing Python docstring style
definitions from the database/languages/python/ directory.
"""

import json
import logging
from pathlib import Path

from mrdr.database.python_styles.schema import (
    PythonStyleEntry,
    PythonStylesDatabase,
)

logger = logging.getLogger(__name__)

DEFAULT_PYTHON_STYLES_PATH = Path("database/languages/python/python_styles.json")


class PythonStyleNotFoundError(Exception):
    """Python style not found.

    Attributes:
        style: The style name that was not found.
        available: List of available style names.
    """

    def __init__(self, style: str, available: list[str]) -> None:
        self.style = style
        self.available = available
        available_text = ", ".join(available) if available else "none"
        super().__init__(f"Style '{style}' not found. Available: {available_text}")


class PythonStylesLoader:
    """Loads and manages Python docstring style definitions.

    Provides access to Python docstring styles including Sphinx,
    Google, NumPy, Epytext, and PEP 257.
    """

    def __init__(self, database_path: Path | str | None = None) -> None:
        """Initialize the Python styles loader.

        Args:
            database_path: Path to the Python styles JSON database file.
                          Defaults to database/languages/python/python_styles.json
        """
        self._path = Path(database_path) if database_path else DEFAULT_PYTHON_STYLES_PATH
        self._database: PythonStylesDatabase | None = None
        self._styles_by_name: dict[str, PythonStyleEntry] = {}
        self._loaded = False

    @property
    def path(self) -> Path:
        """Get the Python styles database path."""
        return self._path

    def load(self) -> PythonStylesDatabase:
        """Load the Python styles database.

        Returns:
            The loaded PythonStylesDatabase.

        Raises:
            FileNotFoundError: If the database file doesn't exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        self._styles_by_name = {}

        if not self._path.exists():
            logger.warning("Python styles database not found: %s", self._path)
            raise FileNotFoundError(f"Python styles database not found: {self._path}")

        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)

        self._database = PythonStylesDatabase.model_validate(data)

        # Build lookup index
        for style in self._database.styles:
            self._styles_by_name[style.name.lower()] = style

        self._loaded = True
        return self._database

    def get_style(self, name: str) -> PythonStyleEntry:
        """Get a Python docstring style by name.

        Args:
            name: The style name (case-insensitive).
                  Valid values: sphinx, google, numpy, epytext, pep257

        Returns:
            The PythonStyleEntry if found.

        Raises:
            PythonStyleNotFoundError: If the style is not found.
        """
        if not self._loaded:
            self.load()

        name_lower = name.lower()
        if name_lower in self._styles_by_name:
            return self._styles_by_name[name_lower]

        raise PythonStyleNotFoundError(name, self.list_styles())

    def list_styles(self) -> list[str]:
        """Get all available style names.

        Returns:
            Sorted list of all style names.
        """
        if not self._loaded:
            self.load()

        return sorted(self._styles_by_name.keys())

    def get_all(self) -> list[PythonStyleEntry]:
        """Get all Python docstring styles.

        Returns:
            List of all PythonStyleEntry objects.
        """
        if not self._loaded:
            self.load()

        return list(self._styles_by_name.values())

    def search(self, query: str) -> list[PythonStyleEntry]:
        """Search styles by name or description.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching PythonStyleEntry objects.
        """
        if not self._loaded:
            self.load()

        query_lower = query.lower()
        results = []

        for style in self._styles_by_name.values():
            if (
                query_lower in style.name.lower()
                or query_lower in style.description.lower()
            ):
                results.append(style)

        return results

    def get_style_with_marker(self, marker_name: str) -> list[PythonStyleEntry]:
        """Get styles that use a specific marker.

        Args:
            marker_name: The marker name to search for (case-insensitive).

        Returns:
            List of styles that use the specified marker.
        """
        if not self._loaded:
            self.load()

        marker_lower = marker_name.lower()
        results = []

        for style in self._styles_by_name.values():
            for marker in style.markers:
                if marker_lower in marker.name.lower():
                    results.append(style)
                    break

        return results

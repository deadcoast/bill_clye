"""JSON renderer for MRDR.

This module provides a renderer implementation that produces valid JSON
output for programmatic consumption and piping.
"""

import json
from typing import Any

from pydantic import BaseModel

from mrdr.database.schema import DocstringEntry


class JSONRenderer:
    """JSON renderer for structured output.

    Produces valid JSON output suitable for programmatic consumption,
    piping to other tools, or integration with external systems.
    """

    def __init__(self, indent: int | None = 2, sort_keys: bool = False) -> None:
        """Initialize the JSON renderer.

        Args:
            indent: Number of spaces for indentation. None for compact output.
            sort_keys: Whether to sort dictionary keys in output.
        """
        self._indent = indent
        self._sort_keys = sort_keys

    def render(self, data: Any, template: str) -> str:
        """Render data as JSON.

        Args:
            data: The data to render (typically DocstringEntry, dict, or list).
            template: The template name (ignored for JSON, all templates
                produce JSON output).

        Returns:
            Valid JSON string representation of the data.
        """
        serializable = self._to_serializable(data)
        return json.dumps(
            serializable,
            indent=self._indent,
            sort_keys=self._sort_keys,
            ensure_ascii=False,
        )

    def supports_rich(self) -> bool:
        """Check if renderer supports Rich formatting.

        Returns:
            False, as JSON output does not use Rich formatting.
        """
        return False

    def _to_serializable(self, data: Any) -> Any:
        """Convert data to JSON-serializable format.

        Args:
            data: Any data to convert.

        Returns:
            JSON-serializable representation of the data.
        """
        if isinstance(data, BaseModel):
            return data.model_dump()
        elif isinstance(data, dict):
            return {k: self._to_serializable(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._to_serializable(item) for item in data]
        elif hasattr(data, "__dict__"):
            return self._to_serializable(data.__dict__)
        else:
            return data

    def render_entry(self, entry: DocstringEntry) -> str:
        """Render a single DocstringEntry as JSON.

        Args:
            entry: The DocstringEntry to render.

        Returns:
            JSON string representation of the entry.
        """
        return self.render(entry, "show")

    def render_list(self, entries: list[DocstringEntry]) -> str:
        """Render a list of DocstringEntry objects as JSON.

        Args:
            entries: List of DocstringEntry objects.

        Returns:
            JSON array string representation.
        """
        return self.render(entries, "list")

    def render_languages(self, languages: list[str]) -> str:
        """Render a list of language names as JSON.

        Args:
            languages: List of language names.

        Returns:
            JSON array string representation.
        """
        return self.render({"languages": sorted(languages), "count": len(languages)}, "list")

"""Base protocol for data sources."""

from typing import Any, Protocol


class DataSource(Protocol):
    """Protocol for data access abstraction.

    DataSources provide a consistent interface for loading and
    querying data from various storage backends.
    """

    def load(self) -> list[dict[str, Any]]:
        """Load all entries from the data source.

        Returns:
            A list of all entries as dictionaries.
        """
        ...

    def query(self, **filters: Any) -> list[dict[str, Any]]:
        """Query entries with filters.

        Args:
            **filters: Key-value pairs to filter entries.

        Returns:
            A list of matching entries as dictionaries.
        """
        ...

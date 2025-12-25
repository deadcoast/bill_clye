"""Advanced Table Renderer component for MRDR.

This module implements the Advanced Table Renderer with filtering,
sorting, pagination, and markdown export capabilities for displaying
database tables in the CLI.
"""

from dataclasses import dataclass, field
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.text import Text


@dataclass
class TableConfig:
    """Configuration for advanced table rendering.

    Attributes:
        columns: List of column names to display (None for all columns).
        filter_field: Field name to filter by.
        filter_value: Value to filter for.
        sort_field: Field name to sort by.
        sort_descending: Whether to sort in descending order.
        page_size: Number of rows per page.
        current_page: Current page number (1-indexed).
    """

    columns: list[str] | None = None
    filter_field: str | None = None
    filter_value: str | None = None
    sort_field: str | None = None
    sort_descending: bool = False
    page_size: int = 20
    current_page: int = 1


@dataclass
class AdvancedTableRenderer:
    """Advanced table renderer with filtering, sorting, and pagination.

    Provides comprehensive table rendering capabilities including:
    - Column filtering (show only specified columns)
    - Row filtering (filter by field=value)
    - Sorting (ascending/descending by field)
    - Pagination (page navigation for large datasets)
    - Markdown export (GFM table format)

    Attributes:
        data: List of dictionaries representing table rows.
        config: TableConfig instance with rendering options.
        title: Optional table title.
    """

    data: list[dict[str, Any]]
    config: TableConfig = field(default_factory=TableConfig)
    title: str = "Master Docstring Table"

    def render(self, console: Console | None = None) -> str:
        """Render the table with all configured options.

        Args:
            console: Optional Rich Console instance.

        Returns:
            Rendered table as a string.
        """
        if console is None:
            console = Console()

        filtered_data = self._apply_filter()
        sorted_data = self._apply_sort(filtered_data)
        paginated_data, total_pages = self._apply_pagination(sorted_data)

        table = self._build_table(paginated_data)

        with console.capture() as capture:
            console.print(table)
            if total_pages > 1:
                console.print(self._render_pagination_hints(total_pages))

        return capture.get()

    def _apply_filter(self) -> list[dict[str, Any]]:
        """Apply row filtering based on config.

        Returns:
            Filtered list of rows.
        """
        if not self.config.filter_field or not self.config.filter_value:
            return self.data

        return [
            row
            for row in self.data
            if str(row.get(self.config.filter_field, "")).lower()
            == self.config.filter_value.lower()
        ]

    def _apply_sort(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Apply sorting based on config.

        Args:
            data: List of rows to sort.

        Returns:
            Sorted list of rows.
        """
        if not self.config.sort_field:
            return data

        return sorted(
            data,
            key=lambda x: str(x.get(self.config.sort_field, "")),
            reverse=self.config.sort_descending,
        )

    def _apply_pagination(
        self, data: list[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], int]:
        """Apply pagination and return page data with total pages.

        Args:
            data: List of rows to paginate.

        Returns:
            Tuple of (page_data, total_pages).
        """
        if not data:
            return [], 1

        total_pages = (len(data) + self.config.page_size - 1) // self.config.page_size
        total_pages = max(1, total_pages)

        # Clamp current_page to valid range
        current_page = max(1, min(self.config.current_page, total_pages))

        start = (current_page - 1) * self.config.page_size
        end = start + self.config.page_size

        return data[start:end], total_pages

    def _build_table(self, data: list[dict[str, Any]]) -> Table:
        """Build the Rich table with configured columns.

        Args:
            data: List of rows to display.

        Returns:
            Rich Table instance.
        """
        table = Table(title=self.title, border_style="cyan")

        if not data:
            table.add_column("No data", style="dim")
            return table

        # Determine columns to display
        all_columns = list(data[0].keys()) if data else []
        columns = self.config.columns if self.config.columns else all_columns

        # Filter to only columns that exist in data
        columns = [col for col in columns if col in all_columns]

        if not columns:
            columns = all_columns

        # Add columns to table
        for col in columns:
            table.add_column(col.replace("_", " ").title(), style="bold")

        # Add rows
        for row in data:
            values = [self._format_cell(row.get(col, "")) for col in columns]
            table.add_row(*values)

        return table

    def _format_cell(self, value: Any) -> str:
        """Format a cell value for display.

        Args:
            value: The cell value to format.

        Returns:
            Formatted string representation.
        """
        if value is None:
            return ""
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)
        if isinstance(value, dict):
            # For nested dicts like syntax, show key info
            if "type" in value:
                return str(value.get("type", ""))
            return str(value)
        return str(value)

    def _render_pagination_hints(self, total_pages: int) -> Text:
        """Render pagination navigation hints.

        Args:
            total_pages: Total number of pages.

        Returns:
            Rich Text with pagination hints.
        """
        text = Text()
        text.append(
            f"Page {self.config.current_page}/{total_pages}", style="bold cyan"
        )
        text.append(" | ", style="dim")
        text.append("(n)", style="bold")
        text.append(" next · ", style="dim")
        text.append("(p)", style="bold")
        text.append(" prev · ", style="dim")
        text.append("(g)", style="bold")
        text.append(" goto", style="dim")
        return text

    def render_plain(self) -> str:
        """Render the table as plain text without ANSI codes.

        Returns:
            Plain text table representation.
        """
        filtered_data = self._apply_filter()
        sorted_data = self._apply_sort(filtered_data)
        paginated_data, total_pages = self._apply_pagination(sorted_data)

        if not paginated_data:
            return "No data"

        # Determine columns
        all_columns = list(paginated_data[0].keys())
        columns = self.config.columns if self.config.columns else all_columns
        columns = [col for col in columns if col in all_columns]

        if not columns:
            columns = all_columns

        # Calculate column widths
        widths = {}
        for col in columns:
            header_width = len(col.replace("_", " ").title())
            max_data_width = max(
                len(self._format_cell(row.get(col, ""))) for row in paginated_data
            )
            widths[col] = max(header_width, max_data_width, 5)

        lines = [self.title, "=" * len(self.title), ""]

        # Header
        header = " | ".join(
            col.replace("_", " ").title().ljust(widths[col]) for col in columns
        )
        lines.append(header)
        lines.append("-" * len(header))

        # Rows
        for row in paginated_data:
            row_str = " | ".join(
                self._format_cell(row.get(col, "")).ljust(widths[col])
                for col in columns
            )
            lines.append(row_str)

        # Pagination
        if total_pages > 1:
            lines.append("")
            lines.append(f"Page {self.config.current_page}/{total_pages}")

        return "\n".join(lines)

    def export_markdown(self) -> str:
        """Export table as GitHub-Flavored Markdown format.

        Returns:
            Markdown table string.
        """
        filtered_data = self._apply_filter()
        sorted_data = self._apply_sort(filtered_data)

        if not sorted_data:
            return "| No data |"

        # Determine columns
        all_columns = list(sorted_data[0].keys())
        columns = self.config.columns if self.config.columns else all_columns
        columns = [col for col in columns if col in all_columns]

        if not columns:
            columns = all_columns

        lines = []

        # Header
        header = "| " + " | ".join(col.replace("_", " ").title() for col in columns) + " |"
        lines.append(header)

        # Separator
        separator = "| " + " | ".join("---" for _ in columns) + " |"
        lines.append(separator)

        # Rows (export all data, not paginated)
        for row in sorted_data:
            row_values = []
            for col in columns:
                value = self._format_cell(row.get(col, ""))
                # Escape pipe characters in markdown
                value = value.replace("|", "\\|")
                row_values.append(value)
            row_str = "| " + " | ".join(row_values) + " |"
            lines.append(row_str)

        return "\n".join(lines)

    def get_total_rows(self) -> int:
        """Get total number of rows after filtering.

        Returns:
            Number of rows after filter is applied.
        """
        return len(self._apply_filter())

    def get_total_pages(self) -> int:
        """Get total number of pages.

        Returns:
            Total page count.
        """
        filtered_count = len(self._apply_filter())
        if filtered_count == 0:
            return 1
        return (filtered_count + self.config.page_size - 1) // self.config.page_size

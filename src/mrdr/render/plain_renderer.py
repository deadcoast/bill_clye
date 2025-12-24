"""Plain text renderer for MRDR.

This module provides a renderer implementation that produces plain text
output without any ANSI escape sequences or Rich formatting.
"""

from typing import Any

from mrdr.database.schema import DocstringEntry


class PlainRenderer:
    """Plain text renderer for terminal output.

    Produces plain text output without ANSI codes, suitable for
    piping, non-TTY environments, or when --plain flag is used.
    """

    def render(self, data: Any, template: str) -> str:
        """Render data using the specified template.

        Args:
            data: The data to render (typically DocstringEntry or dict).
            template: The template name to use for rendering.
                Supported templates: "show", "list", "inspect", "compare"

        Returns:
            The rendered output as plain text without ANSI codes.
        """
        if template == "show":
            return self._render_show(data)
        elif template == "list":
            return self._render_list(data)
        elif template == "inspect":
            return self._render_inspect(data)
        elif template == "compare":
            return self._render_compare(data)
        else:
            return self._render_default(data)

    def supports_rich(self) -> bool:
        """Check if renderer supports Rich formatting.

        Returns:
            False, as this renderer does not support Rich formatting.
        """
        return False

    def _render_show(self, data: DocstringEntry | dict[str, Any]) -> str:
        """Render a docstring entry for display.

        Args:
            data: DocstringEntry or dict with entry data.

        Returns:
            Plain text formatted string.
        """
        if isinstance(data, dict):
            entry = DocstringEntry(**data)
        else:
            entry = data

        lines = [
            f"=== {entry.language} Docstring Syntax ===",
            "",
            f"Language:        {entry.language}",
            f"Start Delimiter: {repr(entry.syntax.start)}",
            f"End Delimiter:   {repr(entry.syntax.end) if entry.syntax.end else 'None (line-based)'}",
            f"Type:            {entry.syntax.type}",
            f"Location:        {entry.syntax.location}",
        ]

        if entry.tags:
            lines.append(f"Tags:            {', '.join(entry.tags)}")

        if entry.conflict_ref:
            lines.append(f"Conflict:        {entry.conflict_ref}")

        if entry.parsing_rule:
            lines.append(f"Parsing Rule:    {entry.parsing_rule}")

        if entry.metadata:
            lines.append(f"Metadata:        {entry.metadata}")

        if entry.example_content:
            lines.extend(["", "Example:", entry.example_content])

        lines.append("")
        return "\n".join(lines)

    def _render_list(self, data: list[str]) -> str:
        """Render a list of languages.

        Args:
            data: List of language names.

        Returns:
            Plain text formatted list.
        """
        lines = ["=== Supported Languages ===", ""]

        for idx, lang in enumerate(sorted(data), 1):
            lines.append(f"  {idx:3}. {lang}")

        lines.extend(["", f"Total: {len(data)} languages", ""])
        return "\n".join(lines)

    def _render_inspect(self, data: dict[str, Any]) -> str:
        """Render detailed inspection output.

        Args:
            data: Dictionary with detailed entry metadata.

        Returns:
            Plain text formatted inspection.
        """
        lines = ["=== Detailed Inspection ===", ""]

        max_key_len = max(len(str(k)) for k in data.keys()) if data else 0

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for k, v in value.items():
                    lines.append(f"    {k}: {v}")
            elif isinstance(value, list):
                value_str = ", ".join(str(v) for v in value) if value else "[]"
                lines.append(f"{key:{max_key_len}}: {value_str}")
            else:
                value_str = str(value) if value is not None else "None"
                lines.append(f"{key:{max_key_len}}: {value_str}")

        lines.append("")
        return "\n".join(lines)

    def _render_compare(self, data: dict[str, Any]) -> str:
        """Render side-by-side comparison of two languages.

        Args:
            data: Dictionary with 'lang1' and 'lang2' DocstringEntry objects.

        Returns:
            Plain text comparison table.
        """
        lang1 = data.get("lang1")
        lang2 = data.get("lang2")

        if not lang1 or not lang2:
            return "Error: Both languages required for comparison\n"

        if isinstance(lang1, dict):
            lang1 = DocstringEntry(**lang1)
        if isinstance(lang2, dict):
            lang2 = DocstringEntry(**lang2)

        # Calculate column widths
        col1_width = max(len(lang1.language), 20)
        col2_width = max(len(lang2.language), 20)

        lines = [
            "=== Language Comparison ===",
            "",
            f"{'Field':<15} | {lang1.language:<{col1_width}} | {lang2.language:<{col2_width}}",
            "-" * (15 + col1_width + col2_width + 6),
            f"{'Start':<15} | {repr(lang1.syntax.start):<{col1_width}} | {repr(lang2.syntax.start):<{col2_width}}",
            f"{'End':<15} | {(repr(lang1.syntax.end) if lang1.syntax.end else 'None'):<{col1_width}} | {(repr(lang2.syntax.end) if lang2.syntax.end else 'None'):<{col2_width}}",
            f"{'Type':<15} | {str(lang1.syntax.type):<{col1_width}} | {str(lang2.syntax.type):<{col2_width}}",
            f"{'Location':<15} | {str(lang1.syntax.location):<{col1_width}} | {str(lang2.syntax.location):<{col2_width}}",
            "",
        ]

        return "\n".join(lines)

    def _render_default(self, data: Any) -> str:
        """Default rendering for unknown templates.

        Args:
            data: Any data to render.

        Returns:
            String representation of the data.
        """
        return str(data) + "\n"

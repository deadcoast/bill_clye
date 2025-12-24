"""Base protocol for renderers."""

from typing import Any, Protocol


class Renderer(Protocol):
    """Protocol for output rendering.

    Renderers transform data into formatted output strings
    suitable for display in various contexts.
    """

    def render(self, data: Any, template: str) -> str:
        """Render data using the specified template.

        Args:
            data: The data to render.
            template: The template name or format to use.

        Returns:
            The rendered output as a string.
        """
        ...

    def supports_rich(self) -> bool:
        """Check if renderer supports Rich formatting.

        Returns:
            True if the renderer supports Rich terminal formatting,
            False otherwise.
        """
        ...

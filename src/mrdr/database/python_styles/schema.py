"""Python styles schema definitions for MRDR.

This module defines the data structures for Python docstring styles
including Sphinx, Google, NumPy, Epytext, and PEP 257.
"""

from pydantic import BaseModel, Field


class PythonStyleMarker(BaseModel):
    """Marker used in a Python docstring style.

    Attributes:
        name: Marker name (e.g., 'param', 'Args').
        syntax: Marker syntax (e.g., ':param name:', 'Args:').
        description: What the marker documents.
    """

    name: str = Field(..., description="Marker name (e.g., 'param')")
    syntax: str = Field(..., description="Marker syntax (e.g., ':param name:')")
    description: str = Field(..., description="What the marker documents")


class PythonStyleEntry(BaseModel):
    """Python docstring style entry.

    Attributes:
        name: Style name (sphinx, google, numpy, epytext, pep257).
        description: Style description.
        markers: List of markers used in this style.
        template_code: Example code with docstring.
        rules: Style-specific rules.
    """

    name: str = Field(
        ..., description="Style name (sphinx, google, numpy, epytext, pep257)"
    )
    description: str = Field(..., description="Style description")
    markers: list[PythonStyleMarker] = Field(
        default_factory=list, description="Markers used in this style"
    )
    template_code: str = Field(..., description="Example code with docstring")
    rules: list[str] = Field(default_factory=list, description="Style-specific rules")


class DatabaseManifest(BaseModel):
    """Database file manifest."""

    manifest_name: str = Field(..., description="Name of the manifest")
    version: str = Field(default="1.0.0", description="Database version")
    schema_origin: str = Field(..., description="Origin document for schema")
    entry_count: int | None = Field(None, description="Number of entries")
    last_updated: str | None = Field(None, description="Last update date")


class PythonStylesDatabase(BaseModel):
    """Python docstring styles database.

    Attributes:
        manifest: Database manifest with version info.
        styles: List of Python docstring style entries.
    """

    manifest: DatabaseManifest = Field(..., description="Database manifest")
    styles: list[PythonStyleEntry] = Field(
        default_factory=list, description="Python docstring styles"
    )

    def get_style_names(self) -> list[str]:
        """Get all available style names.

        Returns:
            List of style names.
        """
        return [style.name for style in self.styles]

    def get_style(self, name: str) -> PythonStyleEntry | None:
        """Get a style by name.

        Args:
            name: The style name (case-insensitive).

        Returns:
            The PythonStyleEntry if found, None otherwise.
        """
        name_lower = name.lower()
        for style in self.styles:
            if style.name.lower() == name_lower:
                return style
        return None

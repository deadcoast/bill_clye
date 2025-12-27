"""Conflict schema definitions for MRDR.

This module defines the data structures for syntax conflict
documentation between programming languages.
"""

from pydantic import BaseModel, Field, field_validator


class ConflictEntry(BaseModel):
    """Syntax conflict entry.

    Documents a delimiter conflict or similarity between programming
    languages that share the same docstring syntax.

    Attributes:
        id: Conflict identifier (e.g., CONFLICT_TRIPLE_QUOTE).
        delimiter: The conflicting delimiter (e.g., '\"\"\"').
        languages: Languages sharing the delimiter (at least 2).
        resolution: How to resolve/distinguish the conflict.
        attachment_rules: Language -> attachment rule mapping.
        description: Optional detailed description.
    """

    id: str = Field(..., description="Conflict identifier")
    delimiter: str = Field(..., description="The conflicting delimiter")
    languages: list[str] = Field(
        ..., min_length=2, description="Languages sharing the delimiter"
    )
    resolution: str = Field(..., description="How to resolve/distinguish")
    attachment_rules: dict[str, str] = Field(
        ..., description="Language -> attachment rule mapping"
    )
    description: str | None = Field(None, description="Detailed description")

    @field_validator("languages")
    @classmethod
    def validate_languages(cls, v: list[str]) -> list[str]:
        """Validate that at least 2 languages are specified."""
        if len(v) < 2:
            raise ValueError("At least 2 languages must be specified for a conflict")
        return v

    @field_validator("attachment_rules")
    @classmethod
    def validate_attachment_rules(cls, v: dict[str, str]) -> dict[str, str]:
        """Validate that attachment rules are not empty."""
        if not v:
            raise ValueError("Attachment rules cannot be empty")
        return v


class DatabaseManifest(BaseModel):
    """Database file manifest."""

    manifest_name: str = Field(..., description="Name of the manifest")
    version: str = Field(default="1.0.0", description="Database version")
    schema_origin: str = Field(..., description="Origin document for schema")
    entry_count: int | None = Field(None, description="Number of entries")
    last_updated: str | None = Field(None, description="Last update date")


class ConflictDatabase(BaseModel):
    """Syntax conflicts database.

    Attributes:
        manifest: Database manifest with version info.
        conflicts: List of conflict entries.
    """

    manifest: DatabaseManifest = Field(..., description="Database manifest")
    conflicts: list[ConflictEntry] = Field(
        default_factory=list, description="Conflict entries"
    )

    def get_conflict_ids(self) -> list[str]:
        """Get all conflict IDs.

        Returns:
            List of conflict IDs.
        """
        return [conflict.id for conflict in self.conflicts]

    def get_conflict(self, conflict_id: str) -> ConflictEntry | None:
        """Get a conflict by ID.

        Args:
            conflict_id: The conflict ID (case-insensitive).

        Returns:
            The ConflictEntry if found, None otherwise.
        """
        conflict_id_upper = conflict_id.upper()
        for conflict in self.conflicts:
            if conflict.id.upper() == conflict_id_upper:
                return conflict
        return None

    def get_conflicts_for_language(self, language: str) -> list[ConflictEntry]:
        """Get all conflicts involving a specific language.

        Args:
            language: The language name (case-insensitive).

        Returns:
            List of conflicts involving the language.
        """
        language_lower = language.lower()
        return [
            conflict
            for conflict in self.conflicts
            if any(lang.lower() == language_lower for lang in conflict.languages)
        ]

    def get_conflicts_for_delimiter(self, delimiter: str) -> list[ConflictEntry]:
        """Get all conflicts for a specific delimiter.

        Args:
            delimiter: The delimiter string.

        Returns:
            List of conflicts for the delimiter.
        """
        return [
            conflict
            for conflict in self.conflicts
            if conflict.delimiter == delimiter
        ]

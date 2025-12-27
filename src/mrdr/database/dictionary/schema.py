"""Dictionary schema definitions for MRDR.

This module defines the dictionary data structures for the MRDR
hierarchy system as defined in docs/dictionary.md.
"""

from enum import Enum

from pydantic import BaseModel, Field


class HierarchyLevel(str, Enum):
    """Hierarchy level types in the dictionary."""

    NAMETYPE = "nametype"
    GRANDPARENT = "grandparent"
    PARENT = "parent"
    CHILD = "child"
    GRANDCHILD = "grandchild"


class DictionaryEntry(BaseModel):
    """Dictionary hierarchy entry.

    Attributes:
        name: Term name (SCREAMINGSNAKE case).
        alias: Short alias (lowercase).
        level: Hierarchy level.
        description: Term description.
        children: List of child term names.
    """

    name: str = Field(..., description="Term name (SCREAMINGSNAKE)")
    alias: str = Field(..., description="Short alias (lowercase)")
    level: HierarchyLevel = Field(..., description="Hierarchy level")
    description: str = Field(..., description="Term description")
    children: list[str] = Field(default_factory=list, description="Child term names")


class DatabaseManifest(BaseModel):
    """Database file manifest."""

    manifest_name: str = Field(..., description="Name of the manifest")
    version: str = Field(default="1.0.0", description="Database version")
    schema_origin: str = Field(..., description="Origin document for schema")
    entry_count: int | None = Field(None, description="Number of entries")
    last_updated: str | None = Field(None, description="Last update date")


class DictionaryDatabase(BaseModel):
    """Complete dictionary database model.

    Attributes:
        manifest: Database manifest with version info.
        nametypes: NAMETYPE definitions (CHD, PNT, GPN).
        definitions: General definitions.
        grandparents: Grandparent level entries.
        parents: Parent level entries.
        children: Child level entries.
        grandchildren: Grandchild level entries.
    """

    manifest: DatabaseManifest = Field(..., description="Database manifest")
    nametypes: list[DictionaryEntry] = Field(
        default_factory=list, description="NAMETYPE definitions"
    )
    definitions: list[DictionaryEntry] = Field(
        default_factory=list, description="General definitions"
    )
    grandparents: list[DictionaryEntry] = Field(
        default_factory=list, description="Grandparent entries"
    )
    parents: list[DictionaryEntry] = Field(
        default_factory=list, description="Parent entries"
    )
    children: list[DictionaryEntry] = Field(
        default_factory=list, description="Child entries"
    )
    grandchildren: list[DictionaryEntry] = Field(
        default_factory=list, description="Grandchild entries"
    )

    def get_all_entries(self) -> list[DictionaryEntry]:
        """Get all entries from all hierarchy levels.

        Returns:
            Combined list of all dictionary entries.
        """
        return (
            self.nametypes
            + self.definitions
            + self.grandparents
            + self.parents
            + self.children
            + self.grandchildren
        )

    def get_entries_by_level(self, level: HierarchyLevel) -> list[DictionaryEntry]:
        """Get entries at a specific hierarchy level.

        Args:
            level: The hierarchy level to filter by.

        Returns:
            List of entries at the specified level.
        """
        level_map = {
            HierarchyLevel.NAMETYPE: self.nametypes,
            HierarchyLevel.GRANDPARENT: self.grandparents,
            HierarchyLevel.PARENT: self.parents,
            HierarchyLevel.CHILD: self.children,
            HierarchyLevel.GRANDCHILD: self.grandchildren,
        }
        return level_map.get(level, [])

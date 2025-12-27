"""UDL loader for MRDR.

This module handles loading and managing UDL definitions from
the database/languages/udl/ directory.
"""

import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field

from mrdr.database.udl.schema import (
    DOLPHIN_OPERATOR,
    WALRUS_OPERATOR,
    UDLDefinition,
    UDLEntry,
    UDLOperator,
)
from mrdr.database.udl.validator import UDLValidationError, UDLValidator

logger = logging.getLogger(__name__)

DEFAULT_UDL_PATH = Path("database/languages/udl")
DEFAULT_UDL_DATABASE_PATH = Path("database/languages/udl/udl_database.json")


class UDLTemplateEntry(BaseModel):
    """UDL template entry from the database JSON."""

    name: str = Field(..., description="UDL identifier name")
    title: str = Field(..., description="UDL title")
    description: str = Field(..., description="UDL description")
    language: str = Field(default="UDL", description="Target language")
    delimiter_open: str = Field(..., description="Opening delimiter")
    delimiter_close: str = Field(..., description="Closing delimiter")
    bracket_open: str = Field(default="(", description="Opening bracket")
    bracket_close: str = Field(default=")", description="Closing bracket")
    operators: list[dict] = Field(default_factory=list, description="Operators")
    examples: list[str] = Field(default_factory=list, description="Examples")


class UDLDatabaseManifest(BaseModel):
    """UDL database manifest."""

    manifest_name: str
    version: str
    schema_origin: str
    entry_count: int | None = None
    last_updated: str | None = None


class UDLDatabase(BaseModel):
    """UDL templates database."""

    manifest: UDLDatabaseManifest
    templates: list[UDLTemplateEntry] = Field(default_factory=list)


class UDLNotFoundError(Exception):
    """UDL definition not found.

    Attributes:
        name: The UDL name that was not found.
        available: List of available UDL names.
    """

    def __init__(self, name: str, available: list[str]) -> None:
        self.name = name
        self.available = available
        available_text = ", ".join(available) if available else "none"
        super().__init__(f"UDL '{name}' not found. Available: {available_text}")


class UDLLoader:
    """Loads and manages UDL definitions from the database.

    UDL definitions can be loaded from the consolidated udl_database.json
    or from individual JSON files in the UDL directory.
    The loader also provides access to built-in operators.
    """

    def __init__(
        self,
        udl_path: Path | str | None = None,
        database_path: Path | str | None = None,
    ) -> None:
        """Initialize the UDL loader.

        Args:
            udl_path: Path to the UDL directory.
                     Defaults to database/languages/udl/
            database_path: Path to the consolidated UDL database JSON file.
                          Defaults to database/languages/udl/udl_database.json
                          If udl_path is provided, database_path defaults to
                          udl_path/udl_database.json
        """
        self._path = Path(udl_path) if udl_path else DEFAULT_UDL_PATH
        
        # If custom udl_path is provided, look for database in that directory
        if udl_path is not None:
            self._database_path = (
                Path(database_path) if database_path 
                else self._path / "udl_database.json"
            )
        else:
            self._database_path = (
                Path(database_path) if database_path else DEFAULT_UDL_DATABASE_PATH
            )
        
        self._entries: dict[str, UDLEntry] = {}
        self._loaded = False

    @property
    def path(self) -> Path:
        """Get the UDL directory path."""
        return self._path

    @property
    def database_path(self) -> Path:
        """Get the UDL database file path."""
        return self._database_path

    @property
    def builtin_operators(self) -> list[UDLOperator]:
        """Get the list of built-in operators."""
        return [DOLPHIN_OPERATOR, WALRUS_OPERATOR]

    def load(self) -> list[UDLEntry]:
        """Load all UDL entries from the database.

        First attempts to load from the consolidated udl_database.json,
        then falls back to loading individual JSON files.

        Returns:
            A list of all valid UDL entries.
        """
        self._entries = {}

        # Try loading from consolidated database first
        if self._database_path.exists():
            try:
                self._load_from_database()
                self._loaded = True
                return list(self._entries.values())
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(
                    "Failed to load UDL database from %s: %s, falling back to individual files",
                    self._database_path,
                    e,
                )

        # Fall back to loading individual JSON files
        if not self._path.exists():
            logger.warning("UDL directory not found: %s", self._path)
            self._loaded = True
            return []

        for json_file in self._path.glob("*.json"):
            # Skip the database file itself
            if json_file.name == "udl_database.json":
                continue
            try:
                entry = self._load_entry(json_file)
                if entry:
                    self._entries[entry.name.lower()] = entry
            except (json.JSONDecodeError, UDLValidationError) as e:
                logger.warning("Failed to load UDL from %s: %s", json_file, e)

        self._loaded = True
        return list(self._entries.values())

    def _load_from_database(self) -> None:
        """Load entries from the consolidated udl_database.json file."""
        with open(self._database_path, encoding="utf-8") as f:
            data = json.load(f)

        db = UDLDatabase.model_validate(data)

        for template in db.templates:
            # Convert operators from dict to UDLOperator
            operators = [
                UDLOperator(
                    name=op.get("name", ""),
                    open=op.get("open", ""),
                    close=op.get("close", ""),
                )
                for op in template.operators
            ]

            definition = UDLDefinition(
                title=template.title,
                descr=template.description,
                lang=template.language,
                delimiter_open=template.delimiter_open,
                delimiter_close=template.delimiter_close,
                bracket_open=template.bracket_open,
                bracket_close=template.bracket_close,
                operators=operators,
            )

            entry = UDLEntry(
                name=template.name,
                definition=definition,
                examples=template.examples,
            )

            self._entries[entry.name.lower()] = entry

    def _load_entry(self, file_path: Path) -> UDLEntry | None:
        """Load a single UDL entry from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            The loaded UDLEntry, or None if loading fails.
        """
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        # Validate the definition
        definition_data = data.get("definition", data)
        definition = UDLValidator.validate_definition_dict(definition_data)

        return UDLEntry(
            name=data.get("name", file_path.stem),
            definition=definition,
            examples=data.get("examples", []),
            created_at=data.get("created_at", ""),
        )

    def get_udl(self, name: str) -> UDLDefinition:
        """Get a UDL definition by name.

        Args:
            name: The UDL name (case-insensitive).

        Returns:
            The UDLDefinition if found.

        Raises:
            UDLNotFoundError: If the UDL is not found.
        """
        if not self._loaded:
            self.load()

        entry = self._entries.get(name.lower())
        if entry:
            return entry.definition

        raise UDLNotFoundError(name, self.list_udls())

    def get_entry(self, name: str) -> UDLEntry:
        """Get a complete UDL entry by name.

        Args:
            name: The UDL name (case-insensitive).

        Returns:
            The UDLEntry if found.

        Raises:
            UDLNotFoundError: If the UDL is not found.
        """
        if not self._loaded:
            self.load()

        entry = self._entries.get(name.lower())
        if entry:
            return entry

        raise UDLNotFoundError(name, self.list_udls())

    def list_udls(self) -> list[str]:
        """Get all registered UDL names.

        Returns:
            A list of UDL names (no duplicates).
        """
        if not self._loaded:
            self.load()

        return sorted(set(self._entries.keys()))

    def get_all(self) -> list[UDLEntry]:
        """Get all UDL entries.

        Returns:
            List of all UDLEntry objects.
        """
        if not self._loaded:
            self.load()

        return list(self._entries.values())

    def save_udl(self, entry: UDLEntry) -> Path:
        """Save a UDL entry to the database.

        Args:
            entry: The UDL entry to save.

        Returns:
            The path to the saved file.
        """
        # Ensure directory exists
        self._path.mkdir(parents=True, exist_ok=True)

        file_path = self._path / f"{entry.name.lower()}.json"

        data = {
            "name": entry.name,
            "definition": {
                "title": entry.definition.title,
                "descr": entry.definition.description,
                "lang": entry.definition.language,
                "delimiter_open": entry.definition.delimiter_open,
                "delimiter_close": entry.definition.delimiter_close,
                "bracket_open": entry.definition.bracket_open,
                "bracket_close": entry.definition.bracket_close,
                "operators": [
                    {"name": op.name, "open": op.open, "close": op.close}
                    for op in entry.definition.operators
                ],
            },
            "examples": entry.examples,
            "created_at": entry.created_at,
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Update cache
        self._entries[entry.name.lower()] = entry

        return file_path

    def create_udl(
        self,
        name: str,
        title: str,
        description: str,
        delimiter_open: str = "<",
        delimiter_close: str = ">",
        language: str = "UDL",
        operators: list[UDLOperator] | None = None,
    ) -> UDLEntry:
        """Create a new UDL entry with default operators.

        Args:
            name: UDL identifier name.
            title: UDL title.
            description: UDL description.
            delimiter_open: Opening delimiter (default '<').
            delimiter_close: Closing delimiter (default '>').
            language: Target language (default 'UDL').
            operators: Custom operators (defaults to dolphin and walrus).

        Returns:
            The created UDLEntry.
        """
        if operators is None:
            operators = [DOLPHIN_OPERATOR, WALRUS_OPERATOR]

        definition = UDLDefinition(
            title=title,
            descr=description,
            lang=language,
            delimiter_open=delimiter_open,
            delimiter_close=delimiter_close,
            operators=operators,
        )

        entry = UDLEntry(
            name=name,
            definition=definition,
        )

        return entry

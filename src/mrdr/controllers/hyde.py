"""Hyde Controller - Back-end data correlation controller.

This module implements the Hyde controller which manages data operations,
metadata queries, and database interactions for the MRDR CLI.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from mrdr.database.loader import DatabaseLoader
from mrdr.database.query import QueryEngine
from mrdr.database.schema import DocstringEntry
from mrdr.database.validation import ValidationCollector, ValidationResult
from mrdr.utils.errors import LanguageNotFoundError, ValidationError


@dataclass
class HydeController:
    """Back-end data correlation controller.

    Manages data operations, metadata queries, and database interactions.
    Provides the data layer that Jekyl controller consumes for rendering.

    Attributes:
        database_path: Optional path to the database file.
        _loader: Internal database loader instance.
        _query_engine: Internal query engine instance.
    """

    database_path: Optional[Path] = None
    _loader: DatabaseLoader = field(init=False, repr=False)
    _query_engine: QueryEngine = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialize internal components after dataclass init."""
        self._loader = DatabaseLoader(self.database_path)
        self._query_engine = QueryEngine(self._loader)

    def query(self, language: str) -> DocstringEntry:
        """Query docstring syntax for a specific language.

        Args:
            language: The programming language name (case-insensitive).

        Returns:
            The DocstringEntry for the specified language.

        Raises:
            LanguageNotFoundError: If the language is not in the database.
        """
        entry = self._query_engine.query_by_language(language)
        if entry is None:
            suggestions = self._query_engine.get_suggestions(language)
            raise LanguageNotFoundError(language, suggestions)
        return entry

    def list_languages(self) -> list[str]:
        """List all supported languages in the database.

        Returns:
            A sorted list of all language names.
        """
        return self._query_engine.list_languages()

    def inspect(self, language: str) -> dict[str, Any]:
        """Get detailed metadata for a language.

        Returns a comprehensive dictionary with all available information
        about the language's docstring syntax, including syntax signature,
        carrier type, attachment rules, and parsing notes.

        Args:
            language: The programming language name (case-insensitive).

        Returns:
            A dictionary containing detailed metadata:
            - language: The language name
            - syntax_signature: Start and end delimiters
            - carrier_type: The syntax type (literal, block, etc.)
            - attachment_location: Where docstring attaches
            - tags: Categorization tags
            - example_content: Example docstring (if available)
            - conflict_ref: Conflicting syntax reference (if any)
            - parsing_rule: Special parsing instructions (if any)
            - metadata: Additional notes (if any)
            - plusrep: Quality grade (if available)

        Raises:
            LanguageNotFoundError: If the language is not in the database.
        """
        entry = self.query(language)

        result: dict[str, Any] = {
            "language": entry.language,
            "syntax_signature": {
                "start": entry.syntax.start,
                "end": entry.syntax.end,
            },
            "carrier_type": entry.syntax.type,
            "attachment_location": entry.syntax.location,
            "tags": entry.tags,
        }

        # Include optional fields only if they have values
        if entry.example_content:
            result["example_content"] = entry.example_content
        if entry.conflict_ref:
            result["conflict_ref"] = entry.conflict_ref
        if entry.parsing_rule:
            result["parsing_rule"] = entry.parsing_rule
        if entry.metadata:
            result["metadata"] = entry.metadata
        if entry.plusrep:
            result["plusrep"] = {
                "tokens": entry.plusrep.tokens,
                "rating": entry.plusrep.rating,
                "label": entry.plusrep.label,
            }

        return result


    def export(self, language: str, format: str = "json") -> str:
        """Export entry in specified format.

        Serializes a language's docstring entry to JSON or YAML format
        with field order preservation.

        Args:
            language: The programming language name (case-insensitive).
            format: Output format, either "json" or "yaml".

        Returns:
            The serialized entry as a string.

        Raises:
            LanguageNotFoundError: If the language is not in the database.
            ValueError: If an unsupported format is specified.
        """
        entry = self.query(language)
        data = entry.model_dump(exclude_none=True)

        if format.lower() == "json":
            return json.dumps(data, indent=2, ensure_ascii=False)
        elif format.lower() == "yaml":
            return yaml.dump(
                data,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def export_all(self, format: str = "json") -> str:
        """Export all entries in specified format.

        Args:
            format: Output format, either "json" or "yaml".

        Returns:
            The serialized entries as a string.

        Raises:
            ValueError: If an unsupported format is specified.
        """
        entries = self._loader.get_entries()
        data = [entry.model_dump(exclude_none=True) for entry in entries]

        if format.lower() == "json":
            return json.dumps(data, indent=2, ensure_ascii=False)
        elif format.lower() == "yaml":
            return yaml.dump(
                data,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def validate_database(self) -> list[ValidationError]:
        """Validate all database entries against schema.

        Loads the database and returns a list of validation errors
        for any entries that fail schema validation.

        Returns:
            A list of ValidationError objects for invalid entries.
            Empty list if all entries are valid.
        """
        # Force reload to capture fresh validation errors
        self._loader._loaded = False
        self._loader.load()

        errors = []
        for entry_name, error_messages in self._loader.validation_errors:
            errors.append(ValidationError(entry_name, error_messages))

        return errors

    def validate_all_databases(self) -> ValidationCollector:
        """Validate all database files against their schemas.

        Loads and validates all database files:
        - docstrings database
        - doctags database
        - dictionary database
        - python_styles database
        - conflict database
        - udl database

        Returns:
            ValidationCollector with results from all databases.
        """
        from mrdr.database.conflict.loader import ConflictLoader
        from mrdr.database.dictionary.loader import DictionaryLoader
        from mrdr.database.doctag.loader import DoctagLoader
        from mrdr.database.python_styles.loader import PythonStylesLoader
        from mrdr.database.udl.loader import UDLLoader

        collector = ValidationCollector()

        # Validate docstrings database
        try:
            self._loader._loaded = False
            self._loader.load()
            if self._loader.validation_result:
                collector.add_result(self._loader.validation_result)
        except FileNotFoundError:
            result = ValidationResult(
                database_type="docstrings",
                database_path=self._loader.path,
            )
            result.add_error(
                entry_id="database",
                message=f"Database file not found: {self._loader.path}",
            )
            collector.add_result(result)
        except Exception as e:
            result = ValidationResult(
                database_type="docstrings",
                database_path=self._loader.path,
            )
            result.add_error(
                entry_id="database",
                message=f"Failed to load database: {e}",
            )
            collector.add_result(result)

        # Validate doctags database
        try:
            doctag_loader = DoctagLoader()
            doctag_loader.load()
            if doctag_loader.validation_result:
                collector.add_result(doctag_loader.validation_result)
        except FileNotFoundError:
            result = ValidationResult(
                database_type="doctags",
                database_path=Path("database/doctags/doctag_database.json"),
            )
            result.add_error(
                entry_id="database",
                message="Database file not found",
            )
            collector.add_result(result)
        except Exception as e:
            result = ValidationResult(
                database_type="doctags",
                database_path=Path("database/doctags/doctag_database.json"),
            )
            result.add_error(
                entry_id="database",
                message=f"Failed to load database: {e}",
            )
            collector.add_result(result)

        # Validate dictionary database
        try:
            dict_loader = DictionaryLoader()
            dict_loader.load()
            if dict_loader.validation_result:
                collector.add_result(dict_loader.validation_result)
        except FileNotFoundError:
            result = ValidationResult(
                database_type="dictionary",
                database_path=Path("database/dictionary/dictionary_database.json"),
            )
            result.add_error(
                entry_id="database",
                message="Database file not found",
            )
            collector.add_result(result)
        except Exception as e:
            result = ValidationResult(
                database_type="dictionary",
                database_path=Path("database/dictionary/dictionary_database.json"),
            )
            result.add_error(
                entry_id="database",
                message=f"Failed to load database: {e}",
            )
            collector.add_result(result)

        # Validate python_styles database
        try:
            styles_loader = PythonStylesLoader()
            styles_loader.load()
            if styles_loader.validation_result:
                collector.add_result(styles_loader.validation_result)
        except FileNotFoundError:
            result = ValidationResult(
                database_type="python_styles",
                database_path=Path("database/languages/python/python_styles.json"),
            )
            result.add_error(
                entry_id="database",
                message="Database file not found",
            )
            collector.add_result(result)
        except Exception as e:
            result = ValidationResult(
                database_type="python_styles",
                database_path=Path("database/languages/python/python_styles.json"),
            )
            result.add_error(
                entry_id="database",
                message=f"Failed to load database: {e}",
            )
            collector.add_result(result)

        # Validate conflict database
        try:
            conflict_loader = ConflictLoader()
            conflict_loader.load()
            if conflict_loader.validation_result:
                collector.add_result(conflict_loader.validation_result)
        except FileNotFoundError:
            result = ValidationResult(
                database_type="conflicts",
                database_path=Path("database/conflicts/conflict_database.json"),
            )
            result.add_error(
                entry_id="database",
                message="Database file not found",
            )
            collector.add_result(result)
        except Exception as e:
            result = ValidationResult(
                database_type="conflicts",
                database_path=Path("database/conflicts/conflict_database.json"),
            )
            result.add_error(
                entry_id="database",
                message=f"Failed to load database: {e}",
            )
            collector.add_result(result)

        # Validate UDL database
        try:
            udl_loader = UDLLoader()
            udl_loader.load()
            if udl_loader.validation_result:
                collector.add_result(udl_loader.validation_result)
        except FileNotFoundError:
            result = ValidationResult(
                database_type="udl",
                database_path=Path("database/languages/udl/udl_database.json"),
            )
            result.add_error(
                entry_id="database",
                message="Database file not found",
            )
            collector.add_result(result)
        except Exception as e:
            result = ValidationResult(
                database_type="udl",
                database_path=Path("database/languages/udl/udl_database.json"),
            )
            result.add_error(
                entry_id="database",
                message=f"Failed to load database: {e}",
            )
            collector.add_result(result)

        return collector

    def get_database_metadata(self) -> dict[str, Any]:
        """Get database manifest metadata.

        Returns:
            Dictionary with manifest_name, version, schema_origin.
        """
        return self._loader.get_metadata()

    def execute(self, command: str, **kwargs: Any) -> Any:
        """Execute a controller command.

        Implements the Controller protocol for command dispatch.

        Args:
            command: The command to execute (query, list, inspect, export, validate).
            **kwargs: Additional arguments for the command.

        Returns:
            The result of the command execution.

        Raises:
            ValueError: If an unknown command is specified.
        """
        commands = {
            "query": lambda: self.query(kwargs["language"]),
            "list": lambda: self.list_languages(),
            "inspect": lambda: self.inspect(kwargs["language"]),
            "export": lambda: self.export(
                kwargs["language"],
                kwargs.get("format", "json"),
            ),
            "export_all": lambda: self.export_all(kwargs.get("format", "json")),
            "validate": lambda: self.validate_database(),
            "validate_all": lambda: self.validate_all_databases(),
            "metadata": lambda: self.get_database_metadata(),
        }

        if command not in commands:
            raise ValueError(f"Unknown command: {command}")

        return commands[command]()

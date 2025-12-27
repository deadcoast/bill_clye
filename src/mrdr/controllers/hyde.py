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
        _doctag_loader: Internal doctag loader instance.
        _dictionary_loader: Internal dictionary loader instance.
        _python_styles_loader: Internal Python styles loader instance.
        _conflict_loader: Internal conflict loader instance.
    """

    database_path: Optional[Path] = None
    _loader: DatabaseLoader = field(init=False, repr=False)
    _query_engine: QueryEngine = field(init=False, repr=False)
    _doctag_loader: Any = field(init=False, repr=False, default=None)
    _dictionary_loader: Any = field(init=False, repr=False, default=None)
    _python_styles_loader: Any = field(init=False, repr=False, default=None)
    _conflict_loader: Any = field(init=False, repr=False, default=None)

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

    # -------------------------------------------------------------------------
    # Doctag Database Access
    # -------------------------------------------------------------------------

    def _get_doctag_loader(self):
        """Get or create the doctag loader instance."""
        if self._doctag_loader is None:
            from mrdr.database.doctag.loader import DoctagLoader
            self._doctag_loader = DoctagLoader()
        return self._doctag_loader

    def get_doctag(self, tag_id: str):
        """Get a doctag by ID.

        Args:
            tag_id: The tag identifier (e.g., "DDL01", "GRM05").

        Returns:
            The DoctagEntry for the requested tag.

        Raises:
            DoctagNotFoundError: If the tag ID is not found.
        """
        return self._get_doctag_loader().get(tag_id)

    def list_doctags(self) -> list[str]:
        """List all available doctag IDs.

        Returns:
            Sorted list of all doctag IDs.
        """
        return self._get_doctag_loader().list_ids()

    def list_doctags_by_category(self, category: str) -> list:
        """Get all doctags in a specific category.

        Args:
            category: The category to filter by (DDL, GRM, IDC, FMT, DOC).

        Returns:
            List of DoctagEntry objects in the category.
        """
        return self._get_doctag_loader().list_by_category(category)

    def search_doctags(self, query: str) -> list:
        """Search doctags by ID, symbol, or short name.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching DoctagEntry objects.
        """
        return self._get_doctag_loader().search(query)

    def get_all_doctags(self) -> list:
        """Get all doctag definitions.

        Returns:
            List of all DoctagEntry objects.
        """
        return self._get_doctag_loader().get_all()

    # -------------------------------------------------------------------------
    # Dictionary Database Access
    # -------------------------------------------------------------------------

    def _get_dictionary_loader(self):
        """Get or create the dictionary loader instance."""
        if self._dictionary_loader is None:
            from mrdr.database.dictionary.loader import DictionaryLoader
            self._dictionary_loader = DictionaryLoader()
        return self._dictionary_loader

    def get_dictionary_term(self, name: str):
        """Get a dictionary term by name or alias.

        Args:
            name: The term name (case-insensitive) or alias.

        Returns:
            The DictionaryEntry if found.

        Raises:
            DictionaryNotFoundError: If the term is not found.
        """
        return self._get_dictionary_loader().get_term(name)

    def get_dictionary_hierarchy_path(self, name: str) -> list:
        """Get the path from root to the specified term.

        Args:
            name: The term name or alias.

        Returns:
            List of DictionaryEntry objects from root to the term.
        """
        return self._get_dictionary_loader().get_hierarchy_path(name)

    def list_dictionary_terms(self) -> list[str]:
        """Get all available dictionary term names.

        Returns:
            Sorted list of all term names.
        """
        return self._get_dictionary_loader().list_terms()

    def get_dictionary_entries_by_level(self, level: str) -> list:
        """Get all dictionary entries at a specific hierarchy level.

        Args:
            level: The hierarchy level (grandparent, parent, child, grandchild).

        Returns:
            List of DictionaryEntry objects at the specified level.
        """
        return self._get_dictionary_loader().get_entries_by_level(level)

    def search_dictionary(self, query: str) -> list:
        """Search dictionary terms by name, alias, or description.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching DictionaryEntry objects.
        """
        return self._get_dictionary_loader().search(query)

    def get_all_dictionary_entries(self) -> list:
        """Get all dictionary entries.

        Returns:
            List of all DictionaryEntry objects.
        """
        return self._get_dictionary_loader().get_all()

    # -------------------------------------------------------------------------
    # Python Styles Database Access
    # -------------------------------------------------------------------------

    def _get_python_styles_loader(self):
        """Get or create the Python styles loader instance."""
        if self._python_styles_loader is None:
            from mrdr.database.python_styles.loader import PythonStylesLoader
            self._python_styles_loader = PythonStylesLoader()
        return self._python_styles_loader

    def get_python_style(self, name: str):
        """Get a Python docstring style by name.

        Args:
            name: The style name (sphinx, google, numpy, epytext, pep257).

        Returns:
            The PythonStyleEntry if found.

        Raises:
            PythonStyleNotFoundError: If the style is not found.
        """
        return self._get_python_styles_loader().get_style(name)

    def list_python_styles(self) -> list[str]:
        """Get all available Python style names.

        Returns:
            Sorted list of all style names.
        """
        return self._get_python_styles_loader().list_styles()

    def get_all_python_styles(self) -> list:
        """Get all Python docstring styles.

        Returns:
            List of all PythonStyleEntry objects.
        """
        return self._get_python_styles_loader().get_all()

    def search_python_styles(self, query: str) -> list:
        """Search Python styles by name or description.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching PythonStyleEntry objects.
        """
        return self._get_python_styles_loader().search(query)

    def get_python_styles_with_marker(self, marker_name: str) -> list:
        """Get Python styles that use a specific marker.

        Args:
            marker_name: The marker name to search for.

        Returns:
            List of styles that use the specified marker.
        """
        return self._get_python_styles_loader().get_style_with_marker(marker_name)

    # -------------------------------------------------------------------------
    # Conflict Database Access
    # -------------------------------------------------------------------------

    def _get_conflict_loader(self):
        """Get or create the conflict loader instance."""
        if self._conflict_loader is None:
            from mrdr.database.conflict.loader import ConflictLoader
            self._conflict_loader = ConflictLoader()
        return self._conflict_loader

    def get_conflict(self, conflict_id: str):
        """Get a conflict by ID.

        Args:
            conflict_id: The conflict ID (case-insensitive).

        Returns:
            The ConflictEntry if found.

        Raises:
            ConflictNotFoundError: If the conflict is not found.
        """
        return self._get_conflict_loader().get_conflict(conflict_id)

    def get_conflicts_for_language(self, language: str) -> list:
        """Get all conflicts involving a specific language.

        Args:
            language: The language name (case-insensitive).

        Returns:
            List of conflicts involving the language.
        """
        return self._get_conflict_loader().get_conflict_for_language(language)

    def list_conflicts(self) -> list[str]:
        """Get all available conflict IDs.

        Returns:
            Sorted list of all conflict IDs.
        """
        return self._get_conflict_loader().list_conflicts()

    def list_conflict_languages(self) -> list[str]:
        """Get all languages with documented conflicts.

        Returns:
            Sorted list of language names.
        """
        return self._get_conflict_loader().list_languages()

    def get_all_conflicts(self) -> list:
        """Get all conflict entries.

        Returns:
            List of all ConflictEntry objects.
        """
        return self._get_conflict_loader().get_all()

    def search_conflicts(self, query: str) -> list:
        """Search conflicts by ID, delimiter, or language.

        Args:
            query: Search query string (case-insensitive).

        Returns:
            List of matching ConflictEntry objects.
        """
        return self._get_conflict_loader().search(query)

    def get_conflicts_for_delimiter(self, delimiter: str) -> list:
        """Get all conflicts for a specific delimiter.

        Args:
            delimiter: The delimiter string.

        Returns:
            List of conflicts for the delimiter.
        """
        return self._get_conflict_loader().get_conflicts_for_delimiter(delimiter)

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
            # Doctag commands
            "get_doctag": lambda: self.get_doctag(kwargs["tag_id"]),
            "list_doctags": lambda: self.list_doctags(),
            "list_doctags_by_category": lambda: self.list_doctags_by_category(kwargs["category"]),
            "search_doctags": lambda: self.search_doctags(kwargs["query"]),
            "get_all_doctags": lambda: self.get_all_doctags(),
            # Dictionary commands
            "get_dictionary_term": lambda: self.get_dictionary_term(kwargs["name"]),
            "get_dictionary_hierarchy_path": lambda: self.get_dictionary_hierarchy_path(kwargs["name"]),
            "list_dictionary_terms": lambda: self.list_dictionary_terms(),
            "get_dictionary_entries_by_level": lambda: self.get_dictionary_entries_by_level(kwargs["level"]),
            "search_dictionary": lambda: self.search_dictionary(kwargs["query"]),
            "get_all_dictionary_entries": lambda: self.get_all_dictionary_entries(),
            # Python styles commands
            "get_python_style": lambda: self.get_python_style(kwargs["name"]),
            "list_python_styles": lambda: self.list_python_styles(),
            "get_all_python_styles": lambda: self.get_all_python_styles(),
            "search_python_styles": lambda: self.search_python_styles(kwargs["query"]),
            "get_python_styles_with_marker": lambda: self.get_python_styles_with_marker(kwargs["marker_name"]),
            # Conflict commands
            "get_conflict": lambda: self.get_conflict(kwargs["conflict_id"]),
            "get_conflicts_for_language": lambda: self.get_conflicts_for_language(kwargs["language"]),
            "list_conflicts": lambda: self.list_conflicts(),
            "list_conflict_languages": lambda: self.list_conflict_languages(),
            "get_all_conflicts": lambda: self.get_all_conflicts(),
            "search_conflicts": lambda: self.search_conflicts(kwargs["query"]),
            "get_conflicts_for_delimiter": lambda: self.get_conflicts_for_delimiter(kwargs["delimiter"]),
        }

        if command not in commands:
            raise ValueError(f"Unknown command: {command}")

        return commands[command]()

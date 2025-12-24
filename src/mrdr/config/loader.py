"""Configuration loader for MRDR CLI.

Handles loading configuration from file, environment variables,
and provides sensible defaults.
"""

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import ValidationError

from mrdr.config.schema import MRDRConfig, OutputFormat


# Default config file location
DEFAULT_CONFIG_PATH = Path.home() / ".mrdr" / "config.yaml"


class ConfigLoader:
    """Loads and manages MRDR configuration.

    Configuration is loaded with the following precedence (highest to lowest):
    1. Environment variables with MRDR_ prefix
    2. User config file (~/.mrdr/config.yaml)
    3. Default values

    Attributes:
        config_path: Path to the configuration file
        config: The loaded MRDRConfig instance
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize the config loader.

        Args:
            config_path: Optional custom path to config file.
                        Defaults to ~/.mrdr/config.yaml
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self._config: Optional[MRDRConfig] = None

    @property
    def config(self) -> MRDRConfig:
        """Get the loaded configuration, loading if necessary."""
        if self._config is None:
            self._config = self.load()
        return self._config

    def load(self) -> MRDRConfig:
        """Load configuration from file and environment.

        Returns:
            MRDRConfig with merged settings from file and environment
        """
        # Start with defaults
        config_dict: dict[str, Any] = {}

        # Load from file if exists
        if self.config_path.exists():
            config_dict = self._load_from_file()

        # Apply environment variable overrides
        config_dict = self._apply_env_overrides(config_dict)

        # Validate and create config
        try:
            return MRDRConfig(**config_dict)
        except ValidationError:
            # Fall back to defaults on validation error
            return MRDRConfig()

    def _load_from_file(self) -> dict[str, Any]:
        """Load configuration from YAML file.

        Returns:
            Dictionary of configuration values
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
        except (yaml.YAMLError, OSError):
            return {}

    def _apply_env_overrides(self, config_dict: dict[str, Any]) -> dict[str, Any]:
        """Apply environment variable overrides to config.

        Environment variables use MRDR_ prefix and underscore for nesting.
        Examples:
            MRDR_DEFAULT_OUTPUT=plain
            MRDR_DEBUG_MODE=true
            MRDR_THEME_PRIMARY_COLOR=blue

        Args:
            config_dict: Base configuration dictionary

        Returns:
            Configuration with environment overrides applied
        """
        env_mappings = {
            "MRDR_DEFAULT_OUTPUT": ("default_output", self._parse_output_format),
            "MRDR_DATABASE_PATH": ("database_path", str),
            "MRDR_SHOW_HINTS": ("show_hints", self._parse_bool),
            "MRDR_DEBUG_MODE": ("debug_mode", self._parse_bool),
            "MRDR_THEME_PRIMARY_COLOR": ("theme.primary_color", str),
            "MRDR_THEME_ACCENT_COLOR": ("theme.accent_color", str),
            "MRDR_THEME_ERROR_COLOR": ("theme.error_color", str),
            "MRDR_THEME_PLUSREP_POSITIVE": ("theme.plusrep_positive", str),
            "MRDR_THEME_PLUSREP_NEGATIVE": ("theme.plusrep_negative", str),
        }

        for env_var, (key_path, converter) in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                try:
                    converted = converter(value)
                    self._set_nested(config_dict, key_path, converted)
                except (ValueError, KeyError):
                    # Skip invalid environment values
                    pass

        return config_dict

    def _set_nested(self, d: dict[str, Any], key_path: str, value: Any) -> None:
        """Set a nested dictionary value using dot notation.

        Args:
            d: Dictionary to modify
            key_path: Dot-separated path (e.g., "theme.primary_color")
            value: Value to set
        """
        keys = key_path.split(".")
        current = d

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Parse a string to boolean.

        Args:
            value: String value to parse

        Returns:
            Boolean interpretation of the string
        """
        return value.lower() in ("true", "1", "yes", "on")

    @staticmethod
    def _parse_output_format(value: str) -> str:
        """Parse and validate output format.

        Args:
            value: String value to parse

        Returns:
            Valid output format string

        Raises:
            ValueError: If format is not valid
        """
        value_lower = value.lower()
        valid_formats = {f.value for f in OutputFormat}
        if value_lower not in valid_formats:
            raise ValueError(f"Invalid output format: {value}")
        return value_lower

    def reload(self) -> MRDRConfig:
        """Force reload configuration from file and environment.

        Returns:
            Freshly loaded MRDRConfig
        """
        self._config = self.load()
        return self._config

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and persist to file.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            value: Value to set

        Raises:
            ValueError: If the key is not a valid configuration key
        """
        # Valid keys for configuration
        valid_keys = {
            "default_output",
            "database_path",
            "show_hints",
            "debug_mode",
            "theme.primary_color",
            "theme.accent_color",
            "theme.error_color",
            "theme.plusrep_positive",
            "theme.plusrep_negative",
        }

        if key not in valid_keys:
            raise ValueError(f"Invalid configuration key: {key}. Valid keys: {sorted(valid_keys)}")

        # Convert value to appropriate type
        converted_value = self._convert_value(key, value)

        # Load existing config from file (not including env overrides)
        config_dict = self._load_from_file()

        # Set the new value
        self._set_nested(config_dict, key, converted_value)

        # Ensure parent directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Write back to file
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)

        # Reload config to pick up changes
        self.reload()

    def _convert_value(self, key: str, value: Any) -> Any:
        """Convert a value to the appropriate type for a config key.

        Args:
            key: Configuration key
            value: Value to convert

        Returns:
            Converted value

        Raises:
            ValueError: If value cannot be converted
        """
        # Boolean keys
        bool_keys = {"show_hints", "debug_mode"}
        if key in bool_keys:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return self._parse_bool(value)
            raise ValueError(f"Invalid boolean value for {key}: {value}")

        # Output format
        if key == "default_output":
            if isinstance(value, str):
                return self._parse_output_format(value)
            raise ValueError(f"Invalid output format: {value}")

        # String keys (paths and colors)
        return str(value)

    def get(self, key: str) -> Any:
        """Get a configuration value by key.

        Args:
            key: Configuration key (supports dot notation for nested keys)

        Returns:
            The configuration value

        Raises:
            KeyError: If the key does not exist
        """
        config = self.config
        keys = key.split(".")

        current: Any = config
        for k in keys:
            if hasattr(current, k):
                current = getattr(current, k)
            else:
                raise KeyError(f"Configuration key not found: {key}")

        # Convert enum to string value
        if isinstance(current, OutputFormat):
            return current.value

        return current

    def show(self) -> dict[str, Any]:
        """Get all configuration values as a dictionary.

        Returns:
            Dictionary of all configuration values
        """
        config = self.config
        return {
            "default_output": config.default_output.value,
            "database_path": config.database_path,
            "show_hints": config.show_hints,
            "debug_mode": config.debug_mode,
            "theme": {
                "primary_color": config.theme.primary_color,
                "accent_color": config.theme.accent_color,
                "error_color": config.theme.error_color,
                "plusrep_positive": config.theme.plusrep_positive,
                "plusrep_negative": config.theme.plusrep_negative,
            },
        }

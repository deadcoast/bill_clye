"""Property tests for configuration loading.

Feature: mrdr-cli-foundation
Properties: 20, 21, 22
Validates: Requirements 9.2, 9.3, 9.6
"""

import os
import tempfile
from pathlib import Path
from typing import Any

import yaml
from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.config import ConfigLoader, MRDRConfig, OutputFormat, ThemeConfig


# Strategy for valid output format values
output_format_strategy = st.sampled_from([f.value for f in OutputFormat])

# Strategy for valid color names
color_strategy = st.sampled_from(["cyan", "green", "red", "blue", "yellow", "magenta", "white"])

# Strategy for boolean values
bool_strategy = st.booleans()

# Strategy for valid theme config
@st.composite
def theme_config_strategy(draw: st.DrawFn) -> dict[str, str]:
    """Generate valid ThemeConfig data."""
    return {
        "primary_color": draw(color_strategy),
        "accent_color": draw(color_strategy),
        "error_color": draw(color_strategy),
        "plusrep_positive": draw(color_strategy),
        "plusrep_negative": draw(color_strategy),
    }


# Strategy for valid config data
@st.composite
def config_data_strategy(draw: st.DrawFn) -> dict[str, Any]:
    """Generate valid MRDRConfig data."""
    config: dict[str, Any] = {}
    
    if draw(st.booleans()):
        config["default_output"] = draw(output_format_strategy)
    if draw(st.booleans()):
        config["theme"] = draw(theme_config_strategy())
    if draw(st.booleans()):
        config["database_path"] = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=("L", "N", "P"))))
    if draw(st.booleans()):
        config["show_hints"] = draw(bool_strategy)
    if draw(st.booleans()):
        config["debug_mode"] = draw(bool_strategy)
    
    return config


@given(config_data=config_data_strategy())
@settings(max_examples=100)
def test_config_loading_from_file(config_data: dict[str, Any]) -> None:
    """Property 20: Config Loading.

    Feature: mrdr-cli-foundation, Property 20: Config Loading
    For any valid configuration file at ~/.mrdr/config.yaml, the CLI SHALL
    apply the specified preferences to subsequent commands.
    **Validates: Requirements 9.2**
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        # Write config to file
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f)
        
        # Load config
        loader = ConfigLoader(config_path=config_path)
        config = loader.load()
        
        # Verify loaded values match file values
        assert isinstance(config, MRDRConfig)
        
        if "default_output" in config_data:
            assert config.default_output.value == config_data["default_output"]
        
        if "show_hints" in config_data:
            assert config.show_hints == config_data["show_hints"]
        
        if "debug_mode" in config_data:
            assert config.debug_mode == config_data["debug_mode"]
        
        if "database_path" in config_data:
            assert config.database_path == config_data["database_path"]
        
        if "theme" in config_data:
            theme_data = config_data["theme"]
            if "primary_color" in theme_data:
                assert config.theme.primary_color == theme_data["primary_color"]
            if "accent_color" in theme_data:
                assert config.theme.accent_color == theme_data["accent_color"]


@given(
    output_format=output_format_strategy,
    debug_mode=bool_strategy,
    show_hints=bool_strategy,
)
@settings(max_examples=100)
def test_environment_variable_override(
    output_format: str,
    debug_mode: bool,
    show_hints: bool,
) -> None:
    """Property 21: Environment Variable Override.

    Feature: mrdr-cli-foundation, Property 21: Environment Variable Override
    For any environment variable with MRDR_ prefix, its value SHALL override
    the corresponding config file setting.
    **Validates: Requirements 9.3**
    """
    # Save original environment
    original_env = {
        "MRDR_DEFAULT_OUTPUT": os.environ.get("MRDR_DEFAULT_OUTPUT"),
        "MRDR_DEBUG_MODE": os.environ.get("MRDR_DEBUG_MODE"),
        "MRDR_SHOW_HINTS": os.environ.get("MRDR_SHOW_HINTS"),
    }
    
    try:
        # Set environment variables
        os.environ["MRDR_DEFAULT_OUTPUT"] = output_format
        os.environ["MRDR_DEBUG_MODE"] = str(debug_mode).lower()
        os.environ["MRDR_SHOW_HINTS"] = str(show_hints).lower()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            
            # Write config with different values
            file_config = {
                "default_output": "json" if output_format != "json" else "plain",
                "debug_mode": not debug_mode,
                "show_hints": not show_hints,
            }
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(file_config, f)
            
            # Load config - env vars should override file
            loader = ConfigLoader(config_path=config_path)
            config = loader.load()
            
            # Verify environment overrides file
            assert config.default_output.value == output_format
            assert config.debug_mode == debug_mode
            assert config.show_hints == show_hints
    
    finally:
        # Restore original environment
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def test_config_defaults_when_no_file() -> None:
    """Test that defaults are used when no config file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "nonexistent" / "config.yaml"
        
        loader = ConfigLoader(config_path=config_path)
        config = loader.load()
        
        # Should have default values
        assert config.default_output == OutputFormat.RICH
        assert config.show_hints is True
        assert config.debug_mode is False
        assert config.database_path == "database/docstrings/docstring_database.json"
        assert config.theme.primary_color == "cyan"


def test_config_property_caching() -> None:
    """Test that config property caches the loaded config."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump({"debug_mode": True}, f)
        
        loader = ConfigLoader(config_path=config_path)
        
        # First access loads config
        config1 = loader.config
        assert config1.debug_mode is True
        
        # Second access returns same instance
        config2 = loader.config
        assert config1 is config2


def test_config_reload() -> None:
    """Test that reload forces fresh load."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump({"debug_mode": False}, f)
        
        loader = ConfigLoader(config_path=config_path)
        config1 = loader.config
        assert config1.debug_mode is False
        
        # Modify file
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump({"debug_mode": True}, f)
        
        # Reload should get new value
        config2 = loader.reload()
        assert config2.debug_mode is True



# Strategy for valid config keys and values
@st.composite
def config_key_value_strategy(draw: st.DrawFn) -> tuple[str, Any]:
    """Generate valid config key-value pairs."""
    key = draw(st.sampled_from([
        "default_output",
        "show_hints",
        "debug_mode",
        "theme.primary_color",
        "theme.accent_color",
    ]))
    
    if key == "default_output":
        value = draw(output_format_strategy)
    elif key in ("show_hints", "debug_mode"):
        value = draw(bool_strategy)
    else:
        value = draw(color_strategy)
    
    return key, value


@given(key_value=config_key_value_strategy())
@settings(max_examples=100)
def test_config_set_persistence(key_value: tuple[str, Any]) -> None:
    """Property 22: Config Set Persistence.

    Feature: mrdr-cli-foundation, Property 22: Config Set Persistence
    For any valid key-value pair, `mrdr config set <key> <value>` SHALL persist
    the value such that subsequent `mrdr config show` displays the updated value.
    **Validates: Requirements 9.6**
    """
    key, value = key_value
    
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        # Create loader and set value
        loader = ConfigLoader(config_path=config_path)
        loader.set(key, value)
        
        # Create new loader to verify persistence
        new_loader = ConfigLoader(config_path=config_path)
        retrieved_value = new_loader.get(key)
        
        # Verify the value was persisted
        if isinstance(value, bool):
            assert retrieved_value == value
        else:
            assert retrieved_value == value


def test_config_set_creates_file() -> None:
    """Test that set creates config file if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "subdir" / "config.yaml"
        
        loader = ConfigLoader(config_path=config_path)
        loader.set("debug_mode", True)
        
        # File should now exist
        assert config_path.exists()
        
        # Value should be persisted
        new_loader = ConfigLoader(config_path=config_path)
        assert new_loader.get("debug_mode") is True


def test_config_set_invalid_key() -> None:
    """Test that set raises error for invalid keys."""
    import pytest
    
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        loader = ConfigLoader(config_path=config_path)
        
        with pytest.raises(ValueError, match="Invalid configuration key"):
            loader.set("invalid_key", "value")


def test_config_show() -> None:
    """Test that show returns all config values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump({
                "default_output": "plain",
                "debug_mode": True,
                "theme": {"primary_color": "blue"},
            }, f)
        
        loader = ConfigLoader(config_path=config_path)
        shown = loader.show()
        
        assert shown["default_output"] == "plain"
        assert shown["debug_mode"] is True
        assert shown["theme"]["primary_color"] == "blue"
        # Defaults should be present
        assert "show_hints" in shown
        assert "database_path" in shown


def test_config_get() -> None:
    """Test that get retrieves config values correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump({
                "default_output": "json",
                "theme": {"accent_color": "magenta"},
            }, f)
        
        loader = ConfigLoader(config_path=config_path)
        
        assert loader.get("default_output") == "json"
        assert loader.get("theme.accent_color") == "magenta"
        # Default values
        assert loader.get("show_hints") is True

"""Property tests for Alert component.

Feature: mrdr-visual-integration, Property 18: Alert Type Styling
Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6
"""

import re

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.components import ALERT_CONFIG, AlertComponent, AlertType


# Strategy for short printable text (message content)
message_text = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(
        whitelist_categories=("L", "N", "P", "S"),
        blacklist_characters="\r\n\t\x00",
    ),
)

# Strategy for alert types
alert_type_strategy = st.sampled_from(list(AlertType))


@given(alert_type=alert_type_strategy, message=message_text)
@settings(max_examples=100)
def test_alert_type_styling(alert_type: AlertType, message: str) -> None:
    """Property 18: Alert Type Styling.

    Feature: mrdr-visual-integration, Property 18: Alert Type Styling
    For any alert type (NOTE, TIP, IMPORTANT, WARNING, CAUTION), the
    Alert_Component SHALL render with the correct icon, color, and title
    as defined in ALERT_CONFIG.
    **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**
    """
    alert = AlertComponent(alert_type=alert_type, message=message)
    output = alert.render()
    config = ALERT_CONFIG[alert_type]

    # Output should contain the icon for this alert type
    assert config["icon"] in output, f"Output should contain icon {config['icon']}"

    # Output should contain the title for this alert type
    assert config["title"] in output, f"Output should contain title {config['title']}"

    # Output should contain the message
    assert message in output, "Output should contain the message"

    # Output should contain panel border characters (Rich Panel)
    assert "╭" in output or "┌" in output, "Output should contain panel border"


@given(alert_type=alert_type_strategy, message=message_text)
@settings(max_examples=100)
def test_alert_plain_output(alert_type: AlertType, message: str) -> None:
    """Property 18: Alert Type Styling - plain text output.

    Feature: mrdr-visual-integration, Property 18: Alert Type Styling
    For any alert type, render_plain SHALL produce output with uppercase
    title in brackets followed by the message, with no ANSI codes.
    **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**
    """
    alert = AlertComponent(alert_type=alert_type, message=message)
    plain = alert.render_plain()
    config = ALERT_CONFIG[alert_type]

    # Plain output should contain uppercase title in brackets
    expected_prefix = f"[{config['title'].upper()}]"
    assert plain.startswith(expected_prefix), f"Plain output should start with {expected_prefix}"

    # Plain output should contain the message
    assert message in plain, "Plain output should contain the message"

    # Plain output should have no ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    assert len(ansi_pattern.findall(plain)) == 0, "Plain output should have no ANSI codes"


@given(alert_type=alert_type_strategy)
@settings(max_examples=50)
def test_alert_config_completeness(alert_type: AlertType) -> None:
    """Property 18: Alert Type Styling - config completeness.

    Feature: mrdr-visual-integration, Property 18: Alert Type Styling
    For any alert type, ALERT_CONFIG SHALL contain icon, color, and title keys.
    **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**
    """
    config = ALERT_CONFIG[alert_type]

    # Config should have all required keys
    assert "icon" in config, "Config should have 'icon' key"
    assert "color" in config, "Config should have 'color' key"
    assert "title" in config, "Config should have 'title' key"

    # Values should be non-empty strings
    assert isinstance(config["icon"], str) and len(config["icon"]) > 0
    assert isinstance(config["color"], str) and len(config["color"]) > 0
    assert isinstance(config["title"], str) and len(config["title"]) > 0


def test_alert_note_styling() -> None:
    """Alert NOTE type SHALL have cyan styling and informational icon.

    **Validates: Requirements 8.1**
    """
    alert = AlertComponent(alert_type=AlertType.NOTE, message="Test note")
    config = alert.get_config()

    assert config["icon"] == "ℹ️", "NOTE should have informational icon"
    assert config["color"] == "cyan", "NOTE should have cyan color"
    assert config["title"] == "Note", "NOTE should have 'Note' title"


def test_alert_tip_styling() -> None:
    """Alert TIP type SHALL have green styling and lightbulb icon.

    **Validates: Requirements 8.2**
    """
    alert = AlertComponent(alert_type=AlertType.TIP, message="Test tip")
    config = alert.get_config()

    assert config["icon"] == "💡", "TIP should have lightbulb icon"
    assert config["color"] == "green", "TIP should have green color"
    assert config["title"] == "Tip", "TIP should have 'Tip' title"


def test_alert_important_styling() -> None:
    """Alert IMPORTANT type SHALL have magenta styling and exclamation icon.

    **Validates: Requirements 8.3**
    """
    alert = AlertComponent(alert_type=AlertType.IMPORTANT, message="Test important")
    config = alert.get_config()

    assert config["icon"] == "❗", "IMPORTANT should have exclamation icon"
    assert config["color"] == "magenta", "IMPORTANT should have magenta color"
    assert config["title"] == "Important", "IMPORTANT should have 'Important' title"


def test_alert_warning_styling() -> None:
    """Alert WARNING type SHALL have yellow styling and warning icon.

    **Validates: Requirements 8.4**
    """
    alert = AlertComponent(alert_type=AlertType.WARNING, message="Test warning")
    config = alert.get_config()

    assert config["icon"] == "⚠️", "WARNING should have warning icon"
    assert config["color"] == "yellow", "WARNING should have yellow color"
    assert config["title"] == "Warning", "WARNING should have 'Warning' title"


def test_alert_caution_styling() -> None:
    """Alert CAUTION type SHALL have red styling and stop icon.

    **Validates: Requirements 8.5**
    """
    alert = AlertComponent(alert_type=AlertType.CAUTION, message="Test caution")
    config = alert.get_config()

    assert config["icon"] == "🛑", "CAUTION should have stop icon"
    assert config["color"] == "red", "CAUTION should have red color"
    assert config["title"] == "Caution", "CAUTION should have 'Caution' title"


def test_alert_renders_rich_panel() -> None:
    """Alert render SHALL use Rich Panel with appropriate border color.

    **Validates: Requirements 8.6**
    """
    for alert_type in AlertType:
        alert = AlertComponent(alert_type=alert_type, message="Test message")
        output = alert.render()

        # Should contain Rich Panel border characters
        assert "╭" in output or "┌" in output, f"{alert_type} should render as panel"
        assert "╯" in output or "┘" in output, f"{alert_type} should render as panel"

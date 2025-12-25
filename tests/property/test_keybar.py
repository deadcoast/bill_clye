"""Property tests for Keybar component.

Feature: mrdr-visual-integration, Property 3: Keybar Keycap Formatting
Validates: Requirements 1.5
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from mrdr.render.components import Keybar


# Strategy for single key character
key_strategy = st.text(
    min_size=1,
    max_size=3,
    alphabet=st.characters(whitelist_categories=("L", "N", "P"), blacklist_characters="\r\n\t\x00[]")
)

# Strategy for action text
action_strategy = st.text(
    min_size=1,
    max_size=20,
    alphabet=st.characters(whitelist_categories=("L", "N"), blacklist_characters="\r\n\t\x00")
)

# Strategy for hint tuple
hint_strategy = st.tuples(key_strategy, action_strategy)


@given(hints=st.lists(hint_strategy, min_size=1, max_size=6))
@settings(max_examples=100)
def test_keybar_keycap_formatting(hints: list[tuple[str, str]]) -> None:
    """Property 3: Keybar Keycap Formatting.

    Feature: mrdr-visual-integration, Property 3: Keybar Keycap Formatting
    For any keybind hint rendered by Keybar_Component, the output SHALL
    contain kbd-style formatting markers around key characters.
    **Validates: Requirements 1.5**
    """
    keybar = Keybar(hints=hints)
    output = keybar.render()

    # Output should contain kbd-style markers for each key
    for key, _ in hints:
        assert f"[{key}]" in output, f"Key '{key}' should be wrapped in brackets"


@given(hints=st.lists(hint_strategy, min_size=1, max_size=6))
@settings(max_examples=100)
def test_keybar_has_kbd_markers(hints: list[tuple[str, str]]) -> None:
    """Property 3: Keybar Keycap Formatting - marker detection.

    Feature: mrdr-visual-integration, Property 3: Keybar Keycap Formatting
    For any keybar with hints, has_kbd_markers() SHALL return True.
    **Validates: Requirements 1.5**
    """
    keybar = Keybar(hints=hints)
    assert keybar.has_kbd_markers(), "Keybar should have kbd markers"


@given(hints=st.lists(hint_strategy, min_size=1, max_size=6))
@settings(max_examples=100)
def test_keybar_plain_no_ansi(hints: list[tuple[str, str]]) -> None:
    """Property 3: Keybar Keycap Formatting - plain mode.

    Feature: mrdr-visual-integration, Property 3: Keybar Keycap Formatting
    For any keybar, render_plain() SHALL contain no ANSI escape sequences.
    **Validates: Requirements 1.5**
    """
    import re

    keybar = Keybar(hints=hints)
    plain = keybar.render_plain()

    # No ANSI escape sequences
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
    assert len(ansi_pattern.findall(plain)) == 0

    # Should still contain key markers
    for key, action in hints:
        assert f"[{key}]" in plain, f"Key '{key}' should be in plain output"
        assert action in plain, f"Action '{action}' should be in plain output"


@given(hints=st.lists(hint_strategy, min_size=1, max_size=6))
@settings(max_examples=50)
def test_keybar_html_output(hints: list[tuple[str, str]]) -> None:
    """Property 3: Keybar Keycap Formatting - HTML output.

    Feature: mrdr-visual-integration, Property 3: Keybar Keycap Formatting
    For any keybar, render_kbd_html() SHALL produce valid HTML with <kbd> tags.
    **Validates: Requirements 1.5**
    """
    keybar = Keybar(hints=hints)
    html = keybar.render_kbd_html()

    # Should contain <kbd> tags for each key
    for key, action in hints:
        assert f"<kbd>{key}</kbd>" in html, f"Key '{key}' should be in <kbd> tag"
        assert action in html, f"Action '{action}' should be in HTML output"


def test_keybar_default_hints() -> None:
    """Keybar SHALL have sensible default hints."""
    keybar = Keybar()

    # Default hints should include common actions
    output = keybar.render_plain()
    assert "search" in output
    assert "quit" in output


def test_keybar_custom_separator() -> None:
    """Keybar SHALL support custom separator."""
    keybar = Keybar(hints=[("a", "action1"), ("b", "action2")], separator=" | ")
    plain = keybar.render_plain()

    assert " | " in plain
    assert "[a]" in plain
    assert "[b]" in plain

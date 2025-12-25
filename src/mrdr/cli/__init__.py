"""CLI module for MRDR."""

from mrdr.cli.error_handlers import (
    display_language_not_found_error,
    display_database_not_found_error,
    display_validation_error,
    display_config_error,
    display_unknown_command_error,
    display_empty_result_error,
    display_unexpected_error,
    handle_mrdr_error,
    log_unexpected_error,
)
from mrdr.cli.visual_commands import (
    VisualOptions,
    apply_visual_options,
    render_content_with_gutter,
    render_entry_as_accordion,
    render_entry_as_card,
    render_entry_with_gutter,
)

__all__ = [
    # Error handlers
    "display_language_not_found_error",
    "display_database_not_found_error",
    "display_validation_error",
    "display_config_error",
    "display_unknown_command_error",
    "display_empty_result_error",
    "display_unexpected_error",
    "handle_mrdr_error",
    "log_unexpected_error",
    # Visual commands
    "VisualOptions",
    "apply_visual_options",
    "render_content_with_gutter",
    "render_entry_as_accordion",
    "render_entry_as_card",
    "render_entry_with_gutter",
]

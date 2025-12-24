"""Base protocol for controllers."""

from typing import Any, Protocol


class Controller(Protocol):
    """Base protocol for all controllers.

    Controllers handle command execution and coordinate between
    data sources and renderers.
    """

    def execute(self, command: str, **kwargs: Any) -> Any:
        """Execute a controller command.

        Args:
            command: The command to execute.
            **kwargs: Additional arguments for the command.

        Returns:
            The result of the command execution.
        """
        ...

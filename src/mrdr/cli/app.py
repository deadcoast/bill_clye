"""Main Typer application for MRDR CLI."""

import typer

from mrdr import __app_name__, __version__

app = typer.Typer(
    name=__app_name__,
    help="MRDR - The Visual Syntax CLI for docstring and syntax database.",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    """Display version and exit."""
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "-v",
        "--version",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """MRDR - The Visual Syntax CLI."""
    pass

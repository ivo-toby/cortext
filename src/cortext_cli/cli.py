"""Main CLI interface for Cortext."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from cortext_cli.commands import check, init, list, embed, search, rag

console = Console()

app = typer.Typer(
    name="cortext",
    help="AI-augmented workspace for knowledge work",
    add_completion=False,
    invoke_without_command=True,
)


@app.callback()
def callback(ctx: typer.Context):
    """
    Cortext: AI-augmented workspace for knowledge work.

    Use 'cortext init' to create a new workspace or 'cortext check' to verify your setup.
    """
    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                "[bold cyan]🧠 Cortext[/bold cyan]\n\n"
                "AI-augmented workspace for knowledge work\n\n"
                "[dim]Commands:[/dim]\n"
                "  [green]cortext init[/green]       Initialize a new workspace\n"
                "  [green]cortext check[/green]      Check required tools\n"
                "  [green]cortext list[/green]       List conversation types\n"
                "  [green]cortext embed[/green]      Embed documents for RAG\n"
                "  [green]cortext search[/green]     Search conversations\n"
                "  [green]cortext rag status[/green] RAG embedding statistics\n"
                "  [green]cortext --help[/green]     Show all commands\n",
                border_style="cyan",
            )
        )


app.command()(check.check)
app.command()(init.init)
app.command(name="list")(list.list_types)
app.command(name="embed")(embed.embed_command)
app.command(name="search")(search.search_command)
app.add_typer(rag.app, name="rag")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()

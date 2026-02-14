"""
InvestAugur CLI Main Entry Point

AI-augmented finance CLI for portfolio tracking and insights.
"""
from pathlib import Path
import click
from rich.console import Console
from dotenv import load_dotenv


def _get_console() -> Console:
    """Return a Rich Console bound to Click's current stdout stream."""
    return Console(file=click.get_text_stream("stdout"))


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable detailed logging")
@click.option(
    "--local-only", is_flag=True, help="Force local mode (use Ollama instead of Vertex AI)"
)
@click.option(
    "--config", type=click.Path(), default=".env", help="Path to config file (defaults to .env)"
)
@click.pass_context
def cli(ctx, verbose, local_only, config):
    """InvestAugur: AI-augmented finance CLI for portfolio tracking and insights."""
    # Store options in context for subcommands to access
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["local_only"] = local_only
    ctx.obj["config_file"] = config

    # Load environment from config file if it exists
    config_path = Path(config)
    if config_path.exists():
        load_dotenv(config_path)
        if verbose:
            console = _get_console()
            console.print(f"[dim]Loaded config from: {config_path}[/dim]")
    elif verbose:
        console = _get_console()
        console.print(f"[yellow]Config file not found: {config_path}[/yellow]")


# Lazy load commands to minimize startup time
@cli.command(name="init")
@click.option("--force", is_flag=True, help="Recreate directories if they exist")
@click.pass_context
def init_cmd(ctx, force):
    """Initialize the app (create local directories, check dependencies)."""
    from cli.commands.init import init_impl

    init_impl(force)


@cli.command()
@click.argument("symbols", nargs=-1)
@click.option("--sheet-id", required=True, help="Google Sheets ID")
@click.option(
    "--output", type=click.Path(), help="Save output to file (stub - not yet implemented)"
)
@click.pass_context
def track(ctx, symbols, sheet_id, output):
    """Track portfolio holdings (pull from Sheets, fetch realtime data)."""
    from cli.commands.track import track_impl

    track_impl(symbols, sheet_id, output)


@cli.command()
@click.option("--query", required=True, help='Analysis query (e.g., "outlook for AAPL")')
@click.option("--symbol", help="Specific stock symbol")
@click.option("--pdf", is_flag=True, help="Generate PDF report")
@click.pass_context
def analyze(ctx, query, symbol, pdf):
    """Perform AI-augmented analysis (with RAG context)."""
    from cli.commands.analyze import analyze_impl

    analyze_impl(query, symbol, pdf)


@cli.command(name="rag-query")
@click.argument("query")
@click.option(
    "--docs-dir",
    default="./research_docs",
    type=click.Path(exists=True),
    help="Path to research documents directory",
)
@click.pass_context
def rag_query(ctx, query, docs_dir):
    """Direct query to local RAG (for testing/research)."""
    from cli.commands.rag_query import rag_query_impl

    rag_query_impl(query, docs_dir)


@cli.command()
@click.option("--session-id", help="Optional session identifier for conversation history")
@click.pass_context
def chat(ctx, session_id):
    """Enter interactive chatbot mode."""
    from cli.commands.chat import chat_impl

    chat_impl(session_id)


if __name__ == "__main__":
    cli()

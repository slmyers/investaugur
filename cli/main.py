"""
InvestAugur CLI Main Entry Point

AI-augmented finance CLI for portfolio tracking and insights.
"""
import os
from pathlib import Path
import click
from rich.console import Console
from dotenv import load_dotenv

# Initialize rich console for styled output
console = Console()

# Context object for passing global state
class Context:
    def __init__(self):
        self.verbose = False
        self.local_only = False
        self.config_file = None

pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable detailed logging'
)
@click.option(
    '--local-only',
    is_flag=True,
    help='Force local mode (use Ollama instead of Vertex AI)'
)
@click.option(
    '--config',
    type=click.Path(),
    default='.env',
    help='Path to config file (defaults to .env)'
)
@click.pass_context
def cli(ctx, verbose, local_only, config):
    """InvestAugur: AI-augmented finance CLI for portfolio tracking and insights."""
    # Ensure context exists
    ctx.obj = Context()
    ctx.obj.verbose = verbose
    ctx.obj.local_only = local_only
    ctx.obj.config_file = config
    
    # Load environment from config file if it exists
    config_path = Path(config)
    if config_path.exists():
        load_dotenv(config_path)
        if verbose:
            console.print(f"[dim]Loaded config from: {config_path}[/dim]")
    elif verbose:
        console.print(f"[yellow]Config file not found: {config_path}[/yellow]")


# Import commands
from cli.commands import init, track, analyze, rag_query, chat

# Register commands
cli.add_command(init.init_cmd)
cli.add_command(track.track)
cli.add_command(analyze.analyze)
cli.add_command(rag_query.rag_query)
cli.add_command(chat.chat)


if __name__ == '__main__':
    cli()

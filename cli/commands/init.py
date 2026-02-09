"""
Init Command

Initialize the InvestAugur application.
"""
import click
from rich.console import Console
from pathlib import Path

console = Console()


@click.command(name='init')
@click.option(
    '--force',
    is_flag=True,
    help='Overwrite existing configs/directories'
)
def init_cmd(force):
    """Initialize the app (create local directories, check dependencies)."""
    try:
        # Create local RAG database directory
        rag_db_path = Path('./local_rag_db')
        if rag_db_path.exists() and not force:
            console.print(f"[yellow]Directory {rag_db_path} already exists. Use --force to overwrite.[/yellow]")
        else:
            rag_db_path.mkdir(exist_ok=True)
            console.print(f"[green]✓[/green] Created directory: {rag_db_path}")
        
        # Create research docs directory
        research_path = Path('./research_docs')
        if not research_path.exists():
            research_path.mkdir(exist_ok=True)
            console.print(f"[green]✓[/green] Created directory: {research_path}")
        
        console.print("[bold green]Initialized successfully![/bold green]")
        console.print("\n[dim]Next steps:[/dim]")
        console.print("[dim]  1. Add research PDFs to ./research_docs[/dim]")
        console.print("[dim]  2. Configure .env file with API keys[/dim]")
        console.print("[dim]  3. Run 'investaugur --help' to see available commands[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error during initialization: {e}[/red]")
        raise click.Abort()

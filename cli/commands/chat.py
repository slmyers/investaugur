"""
Chat Command

Enter interactive chatbot mode.
"""
import click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()


@click.command()
@click.option("--session-id", help="Optional session identifier for conversation history")
def chat(session_id):
    """Enter interactive chatbot mode."""
    try:
        console.print(
            Panel(
                "[bold cyan]InvestAugur Interactive Chat[/bold cyan]\n\n"
                "Ask questions about your portfolio, stocks, or market analysis.\n"
                "Type 'exit' or 'quit' to end the session.",
                border_style="cyan",
            )
        )

        if session_id:
            console.print(f"[dim]Session ID: {session_id}[/dim]\n")

        # Simple interactive loop (stub)
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]")

                if user_input.lower() in ["exit", "quit", "q"]:
                    console.print("[yellow]Ending chat session. Goodbye![/yellow]")
                    break

                # Stub implementation - will integrate with local agent + RAG
                console.print(
                    f"\n[bold blue]AI[/bold blue]: Processing your query: '{user_input}'..."
                )
                console.print("[dim](Full conversational AI with memory coming in Week 2)[/dim]")

                # Mock response
                mock_response = (
                    f"This is a mock response to: {user_input}\n"
                    "In the full version, this will use the Local Agent with LangChain "
                    "and memory to provide contextual, multi-turn conversations."
                )
                console.print(mock_response)

            except KeyboardInterrupt:
                console.print("\n[yellow]Chat interrupted. Goodbye![/yellow]")
                break

    except Exception as e:
        console.print(f"[red]Error in chat mode: {e}[/red]")
        raise click.Abort()

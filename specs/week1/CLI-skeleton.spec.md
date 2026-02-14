# InvestAugur CLI Skeleton Specification

## Overview
This document specifies the initial CLI skeleton for InvestAugur, focusing on the command-line interface structure. It serves as a blueprint for implementation during Week 1 of the project roadmap. The CLI is the primary user interaction point, handling commands for portfolio tracking, analysis, RAG queries, and interactive modes. It must be lightweight, intuitive, and extensible, aligning with the high-level design's emphasis on Python-based simplicity and efficiency on hardware like a MacBook Air M2.

### Scope
- Define core CLI framework and entry point.
- Outline initial commands, arguments, and flags.
- Specify input/output handling, error management, and extensibility.
- Exclude full integrations (e.g., RAG, AI calls)—these will be stubbed or mocked for the skeleton.
- This spec builds toward the prototype phase; full features will be added in later weeks.

### Requirements
- **Framework**: Use Click (Python CLI framework with command decorators and styled output support via rich).
- **Python Version**: 3.10+ (for type hints and compatibility with project deps like LlamaIndex/LangChain).
- **Dependencies**: Minimal—click, rich (for formatted output), python-dotenv (for .env loading).
- **Installation**: The CLI should be installable via `pip install -e .` (editable mode for dev) and runnable as `investaugur` after setup.
- **Performance**: Keep overhead low (<100ms startup); no heavy imports in the main module.
- **Error Handling**: Graceful exits with user-friendly messages; log to stderr for devs.
- **Extensibility**: Modular design—commands in separate modules for easy addition (e.g., in `/cli/commands/`).

## CLI Structure
### Entry Point
- Main file: `cli/main.py`.
- Use Click's group pattern:
  ```python
  import click
  from pathlib import Path
  from dotenv import load_dotenv

  @click.group()
  @click.option('--verbose', '-v', is_flag=True, help='Enable detailed logging')
  @click.option('--local-only', is_flag=True, help='Force local mode')
  @click.option('--config', type=click.Path(), default='.env', help='Path to config file')
  @click.pass_context
  def cli(ctx, verbose, local_only, config):
      """AI-augmented finance CLI for portfolio tracking and insights."""
      # Load .env at startup
      if Path(config).exists():
          load_dotenv(config)

  if __name__ == "__main__":
      cli()
  ```
- Packaging: Use `pyproject.toml` with Poetry for deps; entry point in `scripts` section to make `investaugur` executable.

### Global Options/Flags
- `--verbose / -v`: Enable detailed logging (default: False).
- `--local-only`: Force local mode (use Ollama instead of Vertex AI; default: False).
- `--config FILE`: Path to custom config file (default: .env).
- These apply to all commands via Click's context.

### Commands
Implement as subcommands with stubs for functionality. Each in its own module (e.g., `cli/commands/analyze.py`) and added to the main app.

1. **init**
   - Description: Initialize the app (e.g., create local dirs, check deps).
   - Usage: `investaugur init [--force]`
   - Arguments/Options:
     - `--force`: Overwrite existing configs/dirs (bool, default: False).
   - Output: Confirmation message; creates `./local_rag_db` if needed.
   - Stub: Print "Initialized successfully."

2. **track**
   - Description: Track portfolio holdings (pull from Sheets, fetch realtime data).
   - Usage: `investaugur track --sheet_id ID [SYMBOLS...]`
   - Arguments/Options:
     - `symbols`: Optional stock symbols (list of str).
     - `--sheet_id`: Google Sheets ID (str, required).
     - `--output FILE`: Save to file (str, default: None; else print to terminal).
   - Output: Table of holdings with prices (use rich.Table for formatting).
   - Stub: Mock data table.

3. **analyze**
   - Description: Perform AI-augmented analysis (with RAG context).
   - Usage: `investaugur analyze --query QUERY [--symbol SYMBOL]`
   - Arguments/Options:
     - `query`: Analysis query (str, required, e.g., "outlook for AAPL").
     - `--symbol`: Specific stock (str, optional).
     - `--pdf`: Generate PDF report (bool, default: False).
   - Output: Text response; optional PDF saved locally.
   - Stub: Echo query with mock response.

4. **rag-query**
   - Description: Direct query to local RAG (for testing/research).
   - Usage: `investaugur rag-query QUERY [--dir DIR]`
   - Arguments/Options:
     - `query`: RAG query (str, required).
     - `--dir`: Path to research docs (str, default: "./research_docs").
   - Output: Retrieved contexts + generated response.
   - Stub: Mock retrieval.

5. **chat**
   - Description: Enter interactive chatbot mode.
   - Usage: `investaugur chat [--session_id ID]`
   - Arguments/Options:
     - `--session_id`: Optional session identifier (str, default: None).
   - Behavior: Input loop (> prompt); process via local agent; exit on 'exit'.
   - Output: Conversational responses.
   - Stub: Simple echo loop.

### Input/Output Handling
- **Input**: Support stdin for batch mode (e.g., pipe queries).
- **Output**: Use rich for colors/tables; plain text fallback.
- **Errors**: Custom exceptions (e.g., MissingEnvError); Click handles help/exits.
- **Logging**: Use logging module; verbose mode logs to console.

## Implementation Notes
- **Modularity**: Each command in `/cli/commands/<cmd>.py` with a function decorated by `@click.command()`.
- **Stubs**: Use placeholders with mock data for unimplemented parts (Week 1 focus is on structure).
- **Testing**: Include basic pytest fixtures in `/tests/test_cli.py` (e.g., invoke via click.testing.CliRunner).
- **GitHub Integration**: Commit this spec; reference in README setup instructions.

## Next Steps
- Implement based on this spec.
- Integrate with Local Agent and Basic RAG specs in subsequent PRs.
- Review for alignment with high-level design (e.g., no cloud calls in skeleton).
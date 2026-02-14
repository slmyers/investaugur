# InvestAugur

AI-augmented finance CLI for portfolio tracking and insights.

## Overview

InvestAugur is a command-line interface (CLI) finance application that combines AI foundation models, realtime data feeds, Retrieval-Augmented Generation (RAG) on research documents, and portfolio tracking. It emphasizes the Google Cloud ecosystem for scalability while ensuring sensitive operations remain fully local to mitigate legal and privacy risks.

## Features

- 🤖 AI-driven portfolio analysis and stock insights
- 📊 Realtime finance data integration
- 📚 Local RAG on research documents (keeps proprietary data private)
- 💬 Interactive chatbot mode
- 📈 Google Sheets integration for portfolio tracking
- 📄 PDF report generation

## Installation

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management

### Setup

1. Clone the repository:
```bash
git clone https://github.com/slmyers/investaugur.git
cd investaugur
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

4. Initialize the application:
```bash
poetry run investaugur init
```

## Usage

### Global Options

- `--verbose, -v`: Enable detailed logging
- `--local-only`: Force local mode (use Ollama instead of Vertex AI)
- `--config FILE`: Path to config file (defaults to .env)

### Commands

#### Initialize
```bash
investaugur init [--force]
```
Initialize the app, create local directories, and check dependencies.

#### Track Portfolio
```bash
investaugur track --sheet-id SHEET_ID [SYMBOLS...]
```
Track portfolio holdings from Google Sheets.

#### Analyze
```bash
investaugur analyze --query "QUERY" [--symbol SYMBOL] [--pdf]
```
Perform AI-augmented analysis with RAG context.

#### RAG Query
```bash
investaugur rag-query "QUERY" [--dir PATH]
```
Direct query to local RAG for testing/research.

#### Chat
```bash
investaugur chat [--session-id ID]
```
Enter interactive chatbot mode.

### Examples

```bash
# Track specific stocks
investaugur track --sheet-id abc123 AAPL GOOGL MSFT

# Analyze a stock
investaugur analyze --query "What is the outlook for Apple?" --symbol AAPL

# Interactive mode
investaugur chat

# Query local research documents
investaugur rag-query "What are the key risks for tech stocks?"
```

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black .
poetry run ruff check .
```

## Architecture

The system follows a hybrid local-cloud model:
- **Local Tier**: Handles sensitive data processing (RAG retrieval, query preparation)
- **Cloud Tier**: Leverages Google Cloud (Vertex AI) for advanced AI generation
- **Data Flow**: User input → Local agent → Local RAG → Augmented prompt → Vertex AI → Response

See [docs/high-level.design.md](docs/high-level.design.md) for detailed architecture.

## Roadmap

- [x] Week 1: CLI skeleton + basic structure
- [ ] Week 2: Local agent + RAG integration + Vertex AI
- [ ] Week 3: Google Sheets integration + CSV ingestion
- [ ] Week 4: Advanced features + PDF reports
- [ ] Week 5: Polish + documentation + release

## Contributing

This is a portfolio project. Contributions are welcome! Please see the specs in `/specs` for implementation details.

## License

This project is licensed under the MIT License.

## Documentation

- [High-Level Design](docs/high-level.design.md)
- [CLI Skeleton Spec](specs/week1/CLI-skeleton.spec.md)
- [Basic RAG Spec](specs/week1/basic-rag.spec.md)
- [Local Agent Spec](specs/week1/local-agent.spec.md)

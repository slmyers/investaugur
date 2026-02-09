# InvestAugur High-Level Design Document

## Project Overview
InvestAugur is a command-line interface (CLI) finance application that combines AI foundation models, realtime data feeds, Retrieval-Augmented Generation (RAG) on research documents, and portfolio tracking. It emphasizes the Google Cloud ecosystem for scalability while ensuring sensitive operations (e.g., RAG on proprietary research docs like RBC PDFs) remain fully local to mitigate legal and privacy risks. The application is optimized for lightweight execution on hardware like a MacBook Air M2 with 24GB RAM and will be open-sourced on GitHub as a portfolio project, with demos using public data.

### Objectives
- Deliver AI-driven insights (e.g., portfolio analysis, stock outlooks) augmented by RAG from research documents.
- Integrate realtime finance data (e.g., stock prices, news) and portfolio tracking via Google Sheets.
- Support CSV ingestion from brokers like IBKR and RBC for Activity and Holdings statements, with uploads to Google Sheets.
- Support interactive/chatbot modes for user queries.
- Enable PDF report generation locally or via Google Docs.
- Use Terraform for infrastructure provisioning (local and GCP).
- Ensure scalability for large document corpora without compromising privacy.

### Target Audience
- Individual investors seeking personalized, AI-augmented finance tools.
- Developers/agents collaborating on the project via GitHub (e.g., for extensions or integrations).

## Architecture
### High-Level Components
The system follows a hybrid local-cloud model:
- **Local Tier**: Handles sensitive data processing (RAG retrieval, query preparation, CSV parsing) on the user's machine.
- **Cloud Tier**: Leverages Google Cloud (Vertex AI) for advanced AI generation, with only ephemeral, retrieved context sent in prompts.
- **Data Flow**: User input → Local agent (prep/refine) → Local RAG retrieval → Augmented prompt → Vertex AI generation → Response/PDF output.

#### 1. **CLI Interface**
   - Framework: Typer or Click (Python-based for simplicity).
   - Commands: e.g., `investaugur analyze --symbol AAPL`, `investaugur track --sheet_id XYZ`, `investaugur chat` (interactive mode), `investaugur ingest --file PATH --broker ibkr --type activity --sheet_id ID` (for CSV uploads).
   - Features: Parse inputs, handle flags (e.g., `--local-only` for offline), output to terminal or files.

#### 2. **Local Agent (Query Preparation & Interactivity)**
   - Library: LangChain with Ollama (e.g., Llama 3.1:8b model for lightweight local LLM).
   - Role: 
     - Refine user queries (e.g., add portfolio context from Sheets).
     - Route queries for RAG (e.g., decide indices based on stock/sector/age).
     - Support interactive mode: Multi-turn conversations via input loop.
   - Tools: Integrated with local RAG as a LangChain tool; optional custom tools for Sheets/Finance APIs.
   - Why Local: Runs efficiently on M2 (2-4GB RAM); keeps prep logic private/offline.

#### 3. **Local RAG System (Research Augmentation)**
   - Libraries: LlamaIndex (orchestration), HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2), Chroma/FAISS (vector store), PyMuPDF (PDF parsing).
   - Storage: Persistent on local disk (e.g., `./local_rag_db`).
   - Process: Load PDFs → Add metadata (stock, sector, decade) → Chunk/embed → Index/store.
   - Scaling for Large Corpora (e.g., Decades of Docs):
     - Use multiple indices: One per stock, sector, or age band (e.g., 2010s, 2020s).
     - Query Routing: Local agent decides relevant indices via prompting; combine results.
     - Hierarchical Retrieval: Use LlamaIndex's HierarchicalNodeParser for summary-to-detail structure.
     - Limits: Handles ~200k-400k chunks per index; route to avoid loading everything.
   - Privacy: Proprietary docs (e.g., RBC) never leave the machine; public docs for GitHub demos.
   - Integration: Retrieves chunks locally, injects as context into prompts for Vertex AI.

#### 4. **Foundation Model (AI Generation)**
   - Primary: Google's Gemini (via Vertex AI endpoint, e.g., gemini-1.5-flash).
   - Interaction: Receives augmented prompts (user query + local RAG context) from local agent.
     - No direct RAG access; context is ephemeral in API calls.
     - Custom Prompts: Via LlamaIndex templates (e.g., "Use this context: {rag_chunks} to analyze: {query}").
   - Fallback: Full local mode with Ollama for offline/sensitive queries.
   - No Training: Zero-shot; relies on pre-trained capabilities.

#### 5. **Realtime Data & Integrations**
   - Finance API: Polygon.io or Alpha Vantage (realtime prices, volumes); supplement with Google Sheets' GOOGLEFINANCE.
   - Portfolio Tracking: Google Sheets API (REST or Apps Script as backend; read/write holdings).
   - News Fetching: Google News RSS/Custom Search API, filtered by portfolio holdings.
   - Concurrency: Use asyncio for parallel API calls.
   - **CSV Ingestion Module**: Parses broker-specific CSVs (IBKR/RBC) for Activity Statements (trades, dividends, fees) and Holdings Statements (positions, values). Uses pandas for normalization; handles edge cases like multi-sections or inconsistent formats. Outputs structured data (DataFrames) for upload to Sheets.
   - **Google Sheets Module**: Manages API interactions—authenticate, create/update tabs, append/write data from CSVs or other sources, read ranges, insert formulas (e.g., GOOGLEFINANCE for realtime). Uses google-api-python-client; supports modes like append/overwrite.

#### 6. **Report Generation**
   - Local: ReportLab or WeasyPrint for PDFs (e.g., portfolio summaries).
   - Remote Option: Google Docs API for templated exports.

#### 7. **Infrastructure & Secrets**
   - Management: Terraform for GCP resources (e.g., Vertex AI endpoints, IAM, Secret Manager).
   - Local Resources: Optional for dev (e.g., PDF tools); defined in Terraform if needed.
   - Secrets: .env (python-dotenv); sync to GCP Secret Manager.
   - Deployment: CLI shells out to `terraform apply` for setup.

### Data Flow Example (Analyze Command)
1. CLI receives input (e.g., "analyze AAPL outlook").
2. Local agent refines query (adds context, routes to relevant RAG indices).
3. Local RAG retrieves top chunks (e.g., from AAPL/2020s index).
4. Builds augmented prompt with chunks.
5. Calls Vertex AI to generate response.
6. Outputs to terminal; generates/saves PDF.

### Data Flow Example (Ingest Command)
1. CLI receives CSV path, broker, type, and sheet_id.
2. CSV Ingestion Module parses file into DataFrames.
3. Google Sheets Module uploads DataFrames to specified tabs (e.g., "Holdings" or "Activity").
4. Outputs confirmation.

### Interactive Mode Flow
- Loop: User input → Local agent (prep, memory for context) → RAG retrieval → Vertex AI → Response.
- Exit on 'exit' or similar.

## Development Guidelines
- **Language**: Python 3.x (ecosystem strength for AI/ML).
- **Dependencies**: Managed via Poetry (lockfile for reproducibility).
- **Testing**: Pytest (unit, integration); mock APIs for offline tests.
- **GitHub Structure**:
  - `/cli`: Main application code.
  - `/rag`: Local RAG modules.
  - `/modules`: CSV Ingestion and Google Sheets modules.
  - `/terraform`: Infra as code.
  - `/docs`: This design doc, README.md with setup/demo.
  - `.gitignore`: Exclude .env, local_rag_db, proprietary PDFs.
- **CI/CD**: GitHub Actions for linting (black), testing, Terraform validation.
- **Scalability Notes**: Multi-index RAG for growth; hybrid cloud for non-sensitive data if needed.
- **Security/Compliance**: No proprietary uploads; service accounts for GCP auth.

## Risks & Mitigations
- **Performance**: Monitor M2 RAM; optimize embeddings/chunk sizes.
- **Costs**: Use GCP free tiers; add quotas.
- **Legal**: Local-only for proprietary docs; seek permissions if scaling to cloud.
- **Dependencies**: Fallbacks for APIs (e.g., local mocks).

## Roadmap
1. **Prototype**: CLI skeleton + local agent + basic RAG (1-2 weeks).
2. **Core Integrations**: Sheets (including Google Sheets Module), finance APIs, Vertex AI, CSV Ingestion Module (2 weeks).
3. **Advanced Features**: Multi-index scaling, interactive mode, PDFs (1-2 weeks).
4. **Polish & Deploy**: Tests, docs, GitHub release (1 week).

This document serves as a reference for collaborating agents/developers. For updates, refer to conversation history or iterate via issues/PRs. If the scaling strategy evolves, it enhances without altering the core plan.
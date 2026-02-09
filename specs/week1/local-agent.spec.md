# InvestAugur Local Agent Specification

## Overview
This document specifies the Local Agent component for InvestAugur, which acts as an intelligent front-end for query processing and interactivity. It is a key part of the hybrid architecture, running entirely locally to handle sensitive or preparatory tasks before integrating with cloud-based AI (e.g., Vertex AI). The Local Agent leverages a lightweight LLM to refine user inputs, route queries for RAG, and manage interactive sessions. This spec guides implementation during Week 1 of the project roadmap (Prototype phase), building on the CLI skeleton.

### Scope
- Define the agent's framework, LLM integration, and core functionalities.
- Outline tools (e.g., for RAG integration) and prompting strategies.
- Specify interactive mode and query refinement/routing logic.
- Include stubs for future extensions (e.g., memory for multi-turn chats).
- Exclude full RAG or cloud integrations—these will be added in Week 2; use mocks/stubs here.
- This component aligns with the high-level design's emphasis on privacy (local execution) and efficiency on the M2 MacBook Air.

### Requirements
- **Framework**: LangChain (for agentic workflows, tools, and chaining).
- **Local LLM**: Ollama (e.g., model="llama3.1:8b" for balance of speed/size; fits in 24GB RAM, ~4-8GB usage).
- **Python Version**: 3.10+ (compatible with LangChain and project deps).
- **Dependencies**: langchain, langchain-community, ollama (via pip); minimal to keep lightweight.
- **Performance**: Response times <5s per query on M2; optimize by limiting context size.
- **Error Handling**: Graceful fallbacks (e.g., if Ollama not running, prompt user); log errors.
- **Extensibility**: Modular tools and prompts for easy addition (e.g., future Sheets tool).
- **Privacy**: All operations local; no data sent externally in this module.

## Agent Structure
### Core Setup
- Main file: `agent/local_agent.py`.
- Initialize the agent with LangChain:
  ```python
  from langchain_community.llms import Ollama
  from langchain.agents import initialize_agent, Tool
  from langchain.prompts import PromptTemplate

  # Local LLM
  local_llm = Ollama(model="llama3.1:8b", temperature=0.7)  # Adjustable for creativity

  # Tools (stubbed for now)
  tools = []  # Add RAG tool, etc.

  # Initialize agent
  agent = initialize_agent(
      tools=tools,
      llm=local_llm,
      agent_type="zero-shot-react-description",  # Simple reasoning; upgrade to structured if needed
      verbose=True,  # For dev logging
      handle_parsing_errors=True  # Graceful error handling
  )
  ```
- Prompts: Use templates for consistency (e.g., for refinement, routing).

### Tools
Start with one core tool; expand later.
1. **Local RAG Tool** (Stubbed in Week 1):
   - Name: "Local_RAG".
   - Description: "Use this to retrieve context from local research documents."
   - Function: Lambda or mock that returns stubbed context (e.g., "Mock RAG response"); integrate actual RAG in Week 2.
   - Example:
     ```python
     rag_tool = Tool(
         name="Local_RAG",
         func=lambda q: "Stubbed RAG context for query: " + q,  # Replace with actual index.query
         description="Retrieves relevant chunks from local RAG indices."
     )
     tools.append(rag_tool)
     ```

### Key Functionalities
1. **Query Refinement**:
   - Input: Raw user query from CLI.
   - Process: Use agent to refine (e.g., add context like "based on my portfolio holdings").
   - Prompt Template:
     ```python
     refinement_prompt = PromptTemplate(
         input_variables=["input"],
         template="Refine this finance query for analysis: {input}. Add relevant context like stock symbols or sectors if implied."
     )
     ```
   - Output: Refined query string.
   - Usage: `refined = agent.run(refinement_prompt.format(input=user_query))`.

2. **RAG Query Routing** (For Scaling):
   - Input: Refined query.
   - Process: Agent decides indices/metadata filters (e.g., "2020s" index for recent docs).
   - Prompt Template:
     ```python
     routing_prompt = PromptTemplate(
         input_variables=["query"],
         template="For query: {query}, select RAG indices (e.g., decades, stocks, sectors) and filters. Return JSON: {{'indices': ['2020s', 'AAPL'], 'filters': {{'sector': 'Tech'}}}}"
     )
     ```
   - Output: JSON dict for routing.
   - Stub: Return mock JSON; integrate with multi-indices in Week 3.

3. **Interactive/Chatbot Mode**:
   - Triggered by `investaugur chat` CLI command.
   - Behavior: Input loop with agent processing each turn.
   - Add basic memory (e.g., ConversationChain in LangChain for context retention).
   - Example Loop (in CLI integration):
     ```python
     from langchain.memory import ConversationBufferMemory

     memory = ConversationBufferMemory()
     # Re-init agent with memory if needed

     while True:
         user_input = input("> ")
         if user_input.lower() == 'exit': break
         response = agent.run(user_input)  # Or chain with refinement/routing
         print(f"AI: {response}")
     ```
   - Stub: Simple echo with "Processing..." for Week 1.

## Integration Notes
- **With CLI**: Expose functions like `refine_query(query: str) -> str`, `route_rag(query: str) -> dict`, `run_chat()`.
- **With RAG**: In Week 2, replace stub in rag_tool with actual LlamaIndex query_engine.
- **Testing**: Pytest for unit tests (mock Ollama responses); integration with CLI runner.
- **GitHub**: Commit to `/agent/` dir; reference in main README and high-level design.

## Next Steps
- Implement based on this spec.
- Integrate with CLI Skeleton and Basic RAG specs in the prototype.
- Review for alignment (e.g., ensure local-only execution).
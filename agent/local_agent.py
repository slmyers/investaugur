"""
Local Agent Module

Intelligent query processing using LangChain and Ollama.
This is a stub implementation for Week 1. Full integration in Week 2.
"""


def refine_query(query: str) -> str:
    """
    Refine user query with additional context.

    Args:
        query: Raw user query from CLI

    Returns:
        Refined query string

    Note: This is a stub. Full implementation will use LangChain + Ollama.
    """
    # Stub: Return query as-is for now
    return f"[Refined] {query}"


def route_rag(query: str) -> dict:
    """
    Determine which RAG indices and filters to use for a query.

    Args:
        query: Refined query string

    Returns:
        Dictionary with routing information (indices, filters)

    Note: This is a stub. Full implementation will use agent-based routing.
    """
    # Stub: Return mock routing info
    return {"indices": ["default"], "filters": {}}


def run_chat():
    """
    Run interactive chat mode with conversation memory.

    Note: This is a stub. Full implementation will use LangChain's ConversationChain.
    """
    raise NotImplementedError("Chat mode will be fully implemented in Week 2")


# Placeholder for future LangChain agent initialization
# Will include:
# - Ollama LLM setup (llama3.1:8b)
# - Tool definitions (RAG tool, etc.)
# - Agent initialization with memory
# - Prompt templates for refinement and routing

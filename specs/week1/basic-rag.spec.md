# InvestAugur Basic RAG Specification

## Overview
This document specifies the Basic Retrieval-Augmented Generation (RAG) component for InvestAugur, which enables querying and augmenting responses with context from research documents. The RAG system runs entirely locally to ensure privacy for proprietary materials (e.g., RBC PDFs). It focuses on PDF ingestion, embedding, vector storage, and simple retrieval. This spec guides implementation during Week 1 of the project roadmap (Prototype phase), providing a foundational single-index setup that can be scaled later (e.g., to multiple indices for decades of docs).

### Scope
- Define the core RAG pipeline: Document loading, chunking, embedding, indexing, and querying.
- Outline basic configuration for local execution.
- Include stubs for advanced features (e.g., multi-index routing, hierarchical nodes).
- Support PDF formats primarily (e.g., research reports); extendable to other docs.
- Exclude full agent or cloud integrations—these will be stubbed; focus on standalone testing.
- This component aligns with the high-level design's local tier for sensitivity and efficiency on the M2 MacBook Air.

### Requirements
- **Libraries**: LlamaIndex (core orchestration), HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2 for lightweight, 384-dim vectors), Chroma (vector store for persistence; fallback to FAISS if needed), PyMuPDF (fitz for PDF parsing).
- **Python Version**: 3.10+ (compatible with project deps).
- **Dependencies**: llama-index, llama-index-embeddings-huggingface, llama-index-vector-stores-chroma, pymupdf (via pip).
- **Performance**: Indexing <5-10 minutes for 50-100 PDFs; queries <2s on M2 (24GB RAM); optimize chunk size (~512 tokens).
- **Storage**: Persistent on disk (e.g., `./local_rag_db`); gitignore to avoid committing data.
- **Error Handling**: Handle invalid PDFs, embedding failures; user-friendly messages.
- **Extensibility**: Design for metadata addition (stock/sector/decade) and multi-index in Week 3.
- **Privacy**: No cloud uploads; docs loaded from local dir only.

## RAG Structure
### Core Setup
- Main file: `rag/basic_rag.py`.
- Use LlamaIndex for the pipeline:
  ```python
  from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
  from llama_index.embeddings.huggingface import HuggingFaceEmbedding
  from llama_index.vector_stores.chroma import ChromaVectorStore
  import chromadb  # For client

  # Set global settings
  Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

  # Load documents (PDFs)
  def load_docs(dir_path: str):
      return SimpleDirectoryReader(input_dir=dir_path).load_data()  # Uses PyMuPDF under the hood

  # Build index (stub for single index)
  def build_index(docs, persist_dir: str = "./local_rag_db"):
      chroma_client = chromadb.PersistentClient(path=persist_dir)
      chroma_collection = chroma_client.get_or_create_collection("investaugur_rag")
      vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
      index = VectorStoreIndex.from_documents(docs, storage_context=StorageContext.from_defaults(vector_store=vector_store))
      index.storage_context.persist(persist_dir=persist_dir)
      return index

  # Query (basic retrieval)
  def query_rag(index, query: str, top_k: int = 5):
      query_engine = index.as_query_engine(similarity_top_k=top_k)
      return query_engine.query(query)  # Returns response with source nodes
  ```
- Chunking: Default LlamaIndex (512 tokens); customizable via NodeParser.

### Metadata Handling (Basic)
- Add during loading for future scaling:
  ```python
  for doc in docs:
      doc.metadata = {
          "stock": "extracted_stock",  # Stub: Parse from filename or content
          "sector": "extracted_sector",
          "decade": "2020s"  # Based on date
      }
  ```
- Stub for filtering: Use in query_engine with filters (e.g., MetadataFilters).

### Scaling Stubs
- Multi-Index: Placeholder function to build per-category indices (e.g., by decade).
- Hierarchical: Stub import for HierarchicalNodeParser (activate in Week 3).

## Integration Notes
- **With Local Agent**: Expose as a LangChain Tool (e.g., func=query_rag); stub returns mock context in Week 1.
- **With CLI**: Commands like `rag-query` call build_index (if needed) then query_rag; use dir flag.
- **Testing**: Pytest for unit tests (mock docs, assert embeddings); integration with sample PDFs.
- **GitHub**: Commit to `/rag/` dir; include sample public docs in `/examples/` for demos.

## Next Steps
- Implement based on this spec.
- Integrate with CLI Skeleton and Local Agent in the prototype.
- Expand to multi-index and full agent routing in Week 3.
- Review for alignment (e.g., ensure local persistence and no cloud deps).
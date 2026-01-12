This README is intentionally detailed to document design decisions and tradeoffs for this AI engineering project.
# Agentic AI RAG System (Azure-Ready)

A production-oriented Agentic AI system that uses Retrieval-Augmented Generation (RAG) and tool-calling to answer user queries over internal documents, designed for Azure OpenAI deployment.

## Overview

Organizations often maintain large volumes of internal documentation such as HR policies, operational guidelines, product FAQs, and technical manuals. While this information is critical for day-to-day decision-making, it is typically scattered across documents and difficult to query efficiently.

This project implements an **Agentic AI system with Retrieval-Augmented Generation (RAG)** that allows users to ask natural language questions and receive accurate, grounded answers sourced directly from internal documents.

The system is designed to:
- Decide when a query can be answered directly by a Large Language Model (LLM)
- Retrieve relevant information from indexed documents when needed
- Provide structured, source-backed responses
- Be deployable in a cloud environment using **Azure OpenAI and Azure App Service**

This solution demonstrates a realistic, production-ready approach to building AI agents for enterprise knowledge access rather than a simple chatbot or proof-of-concept.

## High-Level Architecture

The system follows a modular, service-oriented architecture designed for clarity, extensibility, and cloud deployment.

### Architecture Flow

1. **User Query**
   - A user sends a question via the `/ask` API endpoint.

2. **Agent Controller**
   - The agent analyzes the query and decides whether:
     - The question can be answered directly using the LLM, or
     - Additional context is required from internal documents.

3. **Tool Calling (RAG Retrieval)**
   - If document context is needed, the agent invokes the retrieval tool.
   - Relevant document chunks are fetched from a FAISS vector store.

4. **LLM Response Generation**
   - Retrieved context is injected into the prompt.
   - The LLM generates a grounded, structured answer.

5. **Response Output**
   - The API returns the final answer along with the document sources used.

### Core Components

- **FastAPI** – Backend API layer
- **Agent Controller** – Decision-making and orchestration logic
- **RAG Pipeline** – Document chunking, embedding, and retrieval
- **Vector Store (FAISS)** – Efficient similarity search
- **Embedding Service** – Azure OpenAI / OpenAI-compatible embeddings
- **Session Memory** – Lightweight, session-based agent memory

## Key Features

### 1. Agentic Decision-Making
- The AI agent evaluates each user query to decide whether:
  - It can be answered directly by the LLM, or
  - It requires document-based retrieval using RAG.
- This mimics real-world agent behavior with reasoning and tool usage.

### 2. Retrieval-Augmented Generation (RAG)
- Internal documents are embedded and stored in a FAISS vector database.
- Relevant document chunks are dynamically retrieved at query time.
- Retrieved context is injected into the LLM prompt to ensure factual, grounded responses.

### 3. Tool Calling
- The agent invokes retrieval as an explicit tool when needed.
- This separation of reasoning and action improves reliability and explainability.

### 4. Session-Based Memory
- Basic memory is maintained per session to:
  - Preserve conversational context
  - Enable follow-up questions
- Designed to be easily replaceable with Redis or Cosmos DB for production.

### 5. Clean API Contract
- Simple, well-defined API:
  - `POST /ask`
- Returns both:
  - The generated answer
  - The source documents used

### 6. Azure-Ready Architecture
- Designed for deployment on Azure App Service or Azure Functions.
- Secrets managed via environment variables.
- Compatible with Azure OpenAI and Azure-native services.

### 7. Free-Tier Friendly Local Development
- Supports local testing with minimal cost.
- Architecture cleanly separates cloud-only dependencies from core logic.


## Tech Stack

### Backend & API
- **Python 3.10+**
- **FastAPI** – High-performance API framework
- **Gunicorn + Uvicorn** – Production-grade ASGI server

### AI & LLM
- **Azure OpenAI / OpenAI API**
  - Chat Completions (LLM reasoning & response generation)
  - Embeddings (for document retrieval)
- **Prompt Engineering**
  - System + user prompts
  - Context injection
  - Guarded instructions to reduce hallucinations

### Retrieval-Augmented Generation (RAG)
- **FAISS (CPU)** – Vector similarity search
- **Sentence-level chunking**
- **Embedding Service Abstraction**
  - Azure/OpenAI in production
  - Local-friendly fallback supported during development

### Agent Framework (Custom)
- **Agent Controller**
  - Query classification
  - Tool invocation
  - Response orchestration
- **Tooling Layer**
  - Retrieval tool
- **Session Memory**
  - Lightweight in-memory store

### Cloud & Deployment
- **Microsoft Azure App Service (Linux)**
- **Azure OpenAI** (production target)
- **Environment Variables** for secrets
- **Startup Script (`startup.sh`)**

### DevOps & Utilities
- **FAISS index persistence**
- **dotenv** for local configuration
- **GitHub** for version control


## API Specification

### Endpoint

**POST** `/ask`

### Request Body

The API accepts a JSON payload with the following structure:

{
  "query": "string",
  "session_id": "optional string"
}

### Field Descriptions

- **query** (required)  
  The user’s natural language question or instruction sent to the agent.

- **session_id** (optional)  
  A unique identifier used to maintain session-based conversational memory across multiple requests.

### Response Body

```json
{
  "answer": "string",
  "sources": [
    {
      "document": "string",
      "chunk_id": "integer"
    }
  ],
  "session_id": "string"
}
```
### Response Fields

- **answer**:  
  Final response generated by the agent after reasoning and retrieval.

- **sources**:  
  List of documents and chunk identifiers used to generate the response.
  This provides transparency into the retrieval step of the RAG pipeline.

- **session_id**:  
  Identifier returned to maintain conversational context across multiple requests.

### Example Request

{
  "query": "How many paid leaves do employees get?",
  "session_id": "example-session-001"
}

### Example Response

{
  "answer": "Employees are entitled to 20 paid leaves per calendar year.",
  "sources": [
    {
      "document": "Leave_Policy.txt",
      "chunk_id": 0
    }
  ],
  "session_id": "example-session-001"
}

### Notes & Behavior

- The agent dynamically decides whether retrieval is required for a given query.
- If no relevant documents are needed, the LLM responds directly.
- When retrieval is used, document sources are always returned for traceability.
- Session memory is lightweight and designed for short-lived conversational context.
- The API is stateless except for optional session-based memory handling.

## Setup & Local Development

This section describes how to run the project locally for development and testing purposes.
The local setup mirrors the production architecture while remaining cost-efficient and developer-friendly.

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv or equivalent)
- OpenAI or Azure OpenAI API key
- Basic familiarity with FastAPI and REST APIs

### Environment Variables Setup

Create a `.env` file in the project root using the provided `.env.example` as a reference.

Required environment variables:

- `OPENAI_API_KEY`  
  API key for OpenAI or Azure OpenAI.

- `OPENAI_MODEL`  
  Chat model used by the agent (e.g., gpt-4o-mini or equivalent).

- `EMBEDDING_MODEL`  
  Embedding model used for RAG (e.g., text-embedding-3-small).

- `VECTOR_STORE_PATH`  
  Path to the FAISS vector store directory.

For Azure OpenAI deployments, additional variables may be required:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`

### Local Installation Steps

1. Clone the repository:
   git clone <your-repo-url>
   cd ai-agent-rag

2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  (Linux/macOS)
   .venv\Scripts\activate     (Windows)

3. Install dependencies:
   pip install -r requirements.txt

4. Prepare the document data:
   - Place sample documents inside `data/raw_docs/`
   - Run the ingestion script to build the vector store

5. Start the application:
   uvicorn app.main:app --reload

### Running the RAG Ingestion Pipeline

The ingestion pipeline converts documents into vector embeddings and stores them in a FAISS index.

Steps:

1. Add documents to the ingestion directory:
   data/raw_docs/

2. Run the ingestion script:
   python -m app.rag.ingest

3. After successful execution, the following files will be created:
   - data/vector_store/index.faiss
   - data/vector_store/metadata.pkl

These files are used by the retrieval component during query-time.

### Verifying the Local Setup

Once the application is running, you can verify the setup by calling the API.

1. Ensure the server is running:
   uvicorn app.main:app --reload

2. Open a browser or API client (Postman / curl) and send a request:

   POST http://localhost:8000/ask

   Request body:
   {
     "query": "How many paid leaves do employees get?",
     "session_id": "test-session"
   }

3. Expected behavior:
   - The agent processes the query
   - Relevant documents are retrieved (if needed)
   - A grounded response is returned along with document sources

If a valid response is returned, the local setup is complete.

## Azure Deployment Overview

The application is designed to be deployed on Microsoft Azure using Azure App Service (Linux).
The deployment setup mirrors a production-ready AI service with environment-based configuration
and secure secret management.

### Azure Services Used

- **Azure App Service (Linux)**  
  Hosts the FastAPI backend and agent orchestration layer.

- **Azure OpenAI**  
  Provides LLM inference and embedding generation in production.

- **Azure Storage (optional)**  
  Can be used to persist vector stores or logs if required.

- **Azure Monitor (optional)**  
  Used for basic application logging and diagnostics.

The architecture is modular and can be extended to include
Azure AI Search, Cosmos DB, or AKS if needed.

### Deployment Configuration

The application is deployed as a Python web service on Azure App Service (Linux).

Key configuration details:

- **Runtime**: Python 3.10
- **Startup Command**: bash startup.sh
- **Server**: Gunicorn with Uvicorn workers
- **Environment Variables**: Configured via App Service Configuration settings
- **Secrets**: Stored securely as environment variables (no hardcoding)

All configuration is environment-driven to ensure portability across
local, staging, and production environments.

### Environment Variables on Azure

The following environment variables must be configured in the Azure App Service
under **Configuration → Application settings**.

Required variables:

- `OPENAI_API_KEY`  
  API key for OpenAI or Azure OpenAI.

- `OPENAI_MODEL`  
  Chat model used by the agent in production.

- `EMBEDDING_MODEL`  
  Embedding model used for document retrieval.

- `VECTOR_STORE_PATH`  
  Absolute path to the FAISS vector store directory.

For Azure OpenAI deployments, configure the following instead of `OPENAI_API_KEY`:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT_NAME`

No secrets are stored in the codebase.
All sensitive values are injected at runtime via Azure configuration.
### Known Deployment Constraints

- **Cold Starts**:  
  Azure App Service may experience cold starts, especially on lower-tier plans.

- **Dependency Size**:  
  Large ML dependencies (e.g., sentence-transformers, torch) can increase build and startup time.
  For production, embedding generation should rely on Azure OpenAI instead of local models.

- **Vector Store Persistence**:  
  FAISS indexes stored on disk are suitable for demos and small-scale deployments.
  For larger systems, Azure AI Search or managed vector databases are recommended.

- **API Quotas**:  
  OpenAI and Azure OpenAI rate limits apply and must be handled at the application level.

These constraints are documented to clearly distinguish between
a demo-ready deployment and a fully scaled production system.

## Design Decisions

This section outlines the key architectural and implementation decisions made
while building the agentic AI RAG system, along with the rationale behind them.
The focus was on clarity, extensibility, and real-world production alignment.

### Agent-Oriented Architecture

The system is built around an explicit agent controller rather than a
single monolithic request-response pipeline.

Reasons:
- Enables decision-making before generation
- Supports tool calling and extensibility
- Mirrors real-world agentic AI patterns used in production systems
- Allows future addition of multiple tools and agents

This design makes the system more flexible than a traditional
RAG-only architecture.

### RAG over Fine-Tuning

Retrieval-Augmented Generation (RAG) was chosen instead of model fine-tuning
for handling internal documents.

Reasons:
- Internal documents change frequently and should not require retraining
- RAG provides better transparency by exposing source documents
- Lower operational cost compared to fine-tuning
- Faster iteration and easier debugging
- Better alignment with enterprise compliance and governance requirements

This approach ensures responses remain grounded in the latest available data.

### Vector Store Choice (FAISS)

FAISS was selected as the vector store for similarity search in this implementation.

Reasons:
- Lightweight and fast for local and small-scale deployments
- Simple integration with Python-based ML workflows
- No external service dependency, enabling offline and free-tier development
- Suitable for demonstrating RAG concepts clearly

For large-scale or enterprise deployments, FAISS can be replaced with
Azure AI Search or a managed vector database without changing the agent logic.

### Embedding Service Abstraction

The embedding logic is implemented behind a dedicated service layer
instead of being directly coupled to the agent or retrieval logic.

Reasons:
- Allows easy switching between OpenAI, Azure OpenAI, or other providers
- Keeps the RAG pipeline provider-agnostic
- Simplifies testing and future upgrades
- Prevents vendor lock-in at the application core

This abstraction enables the same codebase to support both
local development and cloud-based production deployments.

### Session-Based Memory

The agent uses a lightweight, session-based memory mechanism to maintain
short conversational context.

Reasons:
- Enables follow-up questions within a session
- Avoids introducing external stateful dependencies
- Keeps the system simple and easy to reason about
- Suitable for demo and interview-assignment scope

For production systems, this memory layer can be replaced with
Redis or Azure Cosmos DB without affecting the agent interface.

## Limitations

This section outlines the known limitations of the current implementation.
These are intentional trade-offs made to balance scope, clarity, and time
constraints for an assignment-level project.

### Model & API Limitations

- The system relies on external LLM APIs (OpenAI / Azure OpenAI), which introduces
  dependency on API availability, quotas, and rate limits.
- No retry or exponential backoff logic is implemented for API failures.
- Model responses are non-deterministic and may vary across requests.

---

### Scalability Limitations

- FAISS is used as a local vector store, which is suitable only for small to
  medium document collections.
- Vector indexes are stored on disk and loaded into memory at runtime.
- The current setup is not optimized for horizontal scaling across instances.

For large-scale production systems, a managed vector database such as
Azure AI Search or Pinecone is recommended.

---

### Deployment Constraints

- The demo deployment assumes a correctly configured Azure environment
  with valid API credentials.
- Large ML dependencies increase cold-start times on lower-tier App Service plans.
- GPU acceleration is not used in this deployment.

---

### Security & Governance Limitations

- Authentication and authorization are not implemented.
- No role-based access control (RBAC) is enforced.
- No document-level access filtering is applied.

These features are intentionally excluded to keep the implementation focused
on core agentic and RAG concepts.

---

### Observability Limitations

- Basic logging is implemented, but structured logging and tracing are minimal.
- No automated evaluation or monitoring of response quality is included.
- No alerting or anomaly detection is configured.

---

### Scope Constraints

- Multi-agent collaboration is not implemented.
- Tool calling is limited to document retrieval.
- Multimodal inputs (audio, vision) are out of scope.

Despite these limitations, the system demonstrates a
production-aligned agentic AI architecture with clear extensibility paths.


## Future Improvements

The current implementation is intentionally scoped for clarity and assignment constraints.
The following enhancements would be prioritized in a production-grade system:

- **Managed Vector Store**  
  Replace local FAISS with Azure AI Search or a managed vector database to enable
  horizontal scaling and high availability.

- **Robust Agent Orchestration**  
  Extend the agent to support multiple tools, multi-step planning, and
  multi-agent collaboration for complex workflows.

- **Persistent Memory Layer**  
  Replace in-memory session storage with Redis or Azure Cosmos DB to support
  long-lived conversations and multi-instance deployments.

- **Authentication & Authorization**  
  Add user authentication, role-based access control (RBAC), and
  document-level access filtering.

- **Observability & Evaluation**  
  Introduce structured logging, tracing, automated evaluation metrics,
  and monitoring dashboards for agent behavior and response quality.

- **Cost & Performance Optimization**  
  Add caching, request batching, and rate-limit handling to optimize
  inference cost and latency.

- **CI/CD & Infrastructure as Code**  
  Automate deployments using GitHub Actions and define infrastructure
  using Bicep or Terraform.

These improvements can be implemented incrementally without
changing the core agent or RAG architecture.




## Summary

This project demonstrates the design and implementation of a production-aligned
agentic AI system using Retrieval-Augmented Generation (RAG).

The solution showcases:
- An agent-driven decision layer
- Tool calling for document retrieval
- Session-based memory
- A modular, cloud-ready architecture
- Azure App Service deployment readiness

While scoped intentionally for an assignment, the architecture reflects
real-world AI engineering practices and can be extended to support
enterprise-scale workloads, additional tools, and advanced orchestration.

The project prioritizes clarity, extensibility, and practical design trade-offs
over excessive complexity.







































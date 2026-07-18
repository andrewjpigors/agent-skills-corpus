---
name: rag-production-setup
version: 1.1.0
description: |
  Production-grade RAG (Retrieval-Augmented Generation) systems with FastAPI
  + LangChain + Chroma + Next.js. Use when building RAG chatbots, document
  Q&A systems, knowledge base assistants, or any app where users ask
  questions against a corpus of documents. Covers chunking, embedding,
  vector stores, reranking, evaluation, hybrid search, multi-tenancy,
  conversation memory, GraphRAG, observability, and deployment.
license: MIT
compatibility: claude-code opencode cursor windsurf
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Production RAG Setup Skill

You are a senior AI engineer who builds production RAG systems. You have shipped RAG to real users and learned what actually works vs what looks good in a tutorial.

## Core philosophy

- Retrieval quality beats model quality. A bad retriever with GPT-4 is worse than a good retriever with GPT-3.5.
- Evaluations are not optional. If you cannot measure retrieval and answer quality, you cannot ship.
- Latency matters. Users leave after 8 seconds. Plan for streaming from day one.
- Costs scale with corpus size, not user count. Chunking strategy is a financial decision.
- Simple pipelines win. Don't add LLM routing, multi-hop, or agentic patterns unless measured evals demand it.

## When to use this skill

Trigger this skill when the user asks for:

- RAG, retrieval-augmented generation
- Chat with PDFs, chat with documents, document Q&A
- Knowledge base, knowledge assistant
- Semantic search over a corpus
- Vector database setup
- Embedding pipeline
- LLM chatbot grounded in company data
- Internal AI assistant

## When NOT to use this skill

- Pure chatbots with no retrieval (use a plain LLM wrapper)
- Real-time data fetching (RAG is for static or slow-changing corpora)
- Image/video/audio retrieval (different embedding models, different pipelines)
- Simple full-text search where BM25 alone is sufficient

## Tech stack defaults

These are the defaults. Deviate only when you have a measured reason.

| Component | Default | Why |
|---|---|---|
| Backend | FastAPI | Async, streaming, type-safe, easy to deploy |
| LLM framework | LangChain | Mature, composable, huge ecosystem |
| Embeddings | OpenAI text-embedding-3-small | Cheap, fast, good enough for most cases |
| LLM | GPT-4o-mini for chat, GPT-4o for evals | Cost/quality balance |
| Vector store | Chroma (dev) / pgvector (prod) | Chroma is local and free, pgvector uses existing Postgres |
| Frontend | Next.js 14 App Router | Streaming SSR, good DX, easy deploy |
| Reranker | Cohere rerank-3 (paid) or bge-reranker (self-hosted) | Massive retrieval quality boost |
| Evaluation | RAGAS + custom test set | Industry standard + your own golden set |
| Observability | LangSmith or Langfuse | Traces, cost tracking, user feedback |

## Architecture

```
[Documents] -> [Loader] -> [Chunker] -> [Embeddings] -> [Vector Store]
                                                          |
[User] -> [Next.js UI] -> [FastAPI] -> [Retriever] -> [Reranker] -> [LLM (stream)] -> [UI]
                                         |
                                    [LangSmith trace]
```

## Section 1: Document loading

### Rules

- Store raw documents in object storage (S3, R2, local /data). Never lose the source.
- Extract text with the right loader. PDFPlumber for PDFs, python-docx for Word, md for markdown.
- Preserve metadata: source path, page number, section heading, last-modified.
- Log every load. You will need to re-embed when documents change.

### Loader decision tree

```
Is it PDF?
- Yes -> Are there tables?
    - Yes -> pdfplumber + table extraction
    - No -> PyPDF2 or unstructured
- No
    - Word -> python-docx
    - Markdown -> LangChain's UnstructuredMarkdownLoader
    - HTML -> BeautifulSoup4
    - Confluence/GitHub/Notion -> use official loaders
    - Plain text -> direct read
```

### Code: Universal loader

```python
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    TextLoader,
)
from langchain_core.documents import Document
import hashlib

def load_document(file_path: str) -> list[Document]:
    """Load any supported file type into LangChain Documents with metadata."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(file_path)

    ext = path.suffix.lower()
    loader_map = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".md": UnstructuredMarkdownLoader,
        ".txt": TextLoader,
    }

    if ext not in loader_map:
        raise ValueError(f"Unsupported file type: {ext}")

    loader = loader_map[ext](str(path))
    docs = loader.load()

    # Add stable IDs and source metadata
    for i, doc in enumerate(docs):
        doc.metadata.update({
            "source_file": path.name,
            "source_path": str(path),
            "file_hash": hashlib.md5(path.read_bytes()).hexdigest()[:12],
            "chunk_index": i,
            "loaded_at": datetime.utcnow().isoformat(),
        })
    return docs
```

## Section 2: Chunking strategy

This is where most RAG systems fail. Bad chunking = bad retrieval.

### Rules

- Start with semantic chunking, not fixed-size.
- Chunk size should be 300-500 tokens for most corpora. Smaller for FAQs, larger for long-form docs.
- Overlap should be 10-20% of chunk size.
- Preserve section headings in metadata. Retrieval can filter on them.
- Build a separate title/summary field for each chunk. Embed it alongside the content.

### Chunking strategies

| Strategy | When to use | Library |
|---|---|---|
| Recursive character | Default, most docs | RecursiveCharacterTextSplitter |
| Markdown header | Markdown docs with structure | MarkdownHeaderTextSplitter |
| Semantic | When sentence boundaries matter | SemanticChunker |
| Token-based | When you must hit exact context window | TokenTextSplitter |

### Code: Production chunker

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(
    docs: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 75,
) -> list[Document]:
    """Chunk documents while preserving metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_documents(docs)

    # Reindex chunk order within each source file
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["total_chunks"] = len(chunks)
    return chunks
```

### Tuning chunk size

- Legal/regulatory docs: 800-1200 tokens. Section integrity matters.
- Technical docs/API refs: 300-500 tokens. Each chunk should be one function/concept.
- FAQ/knowledge base: 100-300 tokens. One Q&A pair per chunk.
- Long-form blogs/books: 400-600 tokens. Balance context and precision.

## Section 3: Embedding

### Rules

- OpenAI text-embedding-3-small is the default. Cheap at $0.02/1M tokens.
- Switch to text-embedding-3-large only when evals show clear quality gain.
- Use open-source (bge-large-en, e5-large-v2) when data cannot leave your servers.
- Embed the chunk text plus the document title. Title gives context the chunk may lack.

### Code: Embedding setup

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536,
)

# Self-hosted alternative
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings_local = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": "cuda"},
)
```

### Cost estimation

```
Corpus size (chars) / 4 / 1_000_000 * $0.02 = embedding cost in USD

Example: 10M chars = 2.5M tokens = $0.05 to embed once
```

## Section 4: Vector stores

### Decision matrix

| Store | When to use | Setup time | Cost |
|---|---|---|---|
| Chroma | Local dev, less than 100k chunks | 2 min | Free |
| pgvector | Already using Postgres, less than 10M chunks | 30 min | Existing DB |
| Pinecone | Managed, less than 100M chunks, no ops | 10 min | $70+/mo |
| Weaviate | Hybrid search out of the box | 1 hour | Self-host or $25+/mo |
| Qdrant | High throughput, filtering, open source | 30 min | Self-host or $25+/mo |

### Code: Chroma setup

```python
import chromadb
from langchain_chroma import Chroma

client = chromadb.PersistentClient(path="./.chroma")

vector_store = Chroma(
    client=client,
    collection_name="knowledge_base",
    embedding_function=embeddings,
)

vector_store.add_documents(chunks)

results = vector_store.similarity_search_with_relevance_scores(
    query="How do I configure SSO?",
    k=10,
)
```

### Code: pgvector setup (production)

```python
from langchain_postgres import PGVector

vector_store = PGVector(
    connection="postgresql+psycopg://user:pass@host/db",
    collection_name="knowledge_base",
    embeddings=embeddings,
    use_jsonb=True,
)
```

### Indexing tips

- HNSW index for most cases. Faster queries, slower build.
- IVFFlat for very large corpora (10M+ vectors). Faster build, slower queries.
- Set ef_construction=128 minimum. Lower kills recall.
- Always measure recall@k before and after index changes.

## Section 5: Retrieval

### Rules

- Top-k from vector search is not enough. Always rerank.
- Hybrid search (vector + BM25) beats pure vector on most corpora. Use it.
- Metadata filters are free relevance. Use them aggressively.
- Return parent documents, not chunks. Use ParentDocumentRetriever.

### Code: Hybrid search

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

bm25 = BM25Retriever.from_documents(chunks)
bm25.k = 10

vector = vector_store.as_retriever(search_kwargs={"k": 10})

ensemble = EnsembleRetriever(
    retrievers=[bm25, vector],
    weights=[0.4, 0.6],
)
```

### Code: Reranker (the highest-ROI upgrade)

```python
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever

reranker = CohereRerank(
    model="rerank-english-v3.0",
    top_n=4,
)

retriever = ContextualCompressionRetriever(
    base_retriever=ensemble,
    base_compressor=reranker,
)
```

### Self-hosted reranker (free)

```python
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-large")
reranker = CrossEncoderReranker(model=model, top_n=4)
```

### Query rewriting (HyDE)

HyDE (Hypothetical Document Embeddings) generates a hypothetical answer to the query, then embeds that answer instead of the raw query. This bridges the vocabulary gap between question and document.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

hyde_prompt = ChatPromptTemplate.from_messages([
    ("system", "Generate a hypothetical answer to the user's question. "
               "Write it as if you found the exact passage in a document. "
               "Do not add preamble. Just the passage."),
    ("human", "{question}"),
])

hyde_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def rewrite_query(question: str) -> str:
    """Rewrite query using HyDE for better retrieval."""
    response = hyde_llm.invoke(hyde_prompt.format(question=question))
    return response.content

# Use in retrieval
def retrieve_with_hyde(question: str):
    rewritten = rewrite_query(question)
    docs = retriever.invoke(rewritten)
    return docs
```

When to use HyDE:
- Queries are short or vague ("how does pricing work?")
- Corpus uses different terminology than users ("SLA" vs "uptime guarantee")
- Measured evals show 20%+ improvement in recall

When to skip:
- Queries are already detailed and match document vocabulary
- Latency budget is tight (adds 200-500ms)

## Section 6: Generation

### Rules

- Always stream. Always. Users tolerate 30 seconds of streaming, they leave after 8 seconds of waiting.
- Show source citations in the UI. Without them, users don't trust the answer.
- Constrain the LLM to refuse when retrieval returns nothing relevant. Hallucination is worse than "I don't know".
- Use GPT-4o-mini for chat. Use GPT-4o only for evaluation/scoring.

### Code: Streaming chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

SYSTEM_PROMPT = """You are a helpful assistant answering questions based on the provided context.

Rules:
- Only use information from the context. If the context doesn't contain the answer, say "I don't know based on the documents I have."
- Cite sources using [Doc N] format corresponding to the listed sources.
- Be concise. Maximum 3 sentences unless the user asks for more.

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}"),
])

def format_docs(docs):
    return "\n\n".join(
        f"[Doc {i+1}] Source: {d.metadata['source_file']}\n{d.page_content}"
        for i, d in enumerate(docs)
    )

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

for chunk in chain.stream("How do I reset my password?"):
    print(chunk, end="", flush=True)
```

## Section 7: Multi-turn conversation with memory

Real users ask follow-up questions. "Tell me more about that" and "What about the pricing?" are common. Without conversation memory, each query is treated as standalone and retrieval fails.

### Code: Conversation chain with memory

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer",
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
)

# First question
result = qa_chain.invoke({"question": "What is your refund policy?"})
# Second question (uses memory)
result2 = qa_chain.invoke({"question": "How many days does that take?"})
# The chain knows "that" refers to "refund"
```

### Code: Redis-backed memory (production)

```python
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

def get_session_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379",
        ttl=3600,  # 1 hour
    )

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# Usage
chain_with_history.invoke(
    {"question": "What is your refund policy?"},
    config={"configurable": {"session_id": "user-123"}},
)
```

### Standalone question rewriting

Follow-up questions like "How much is it?" need rewriting for retrieval to work:

```python
from langchain_core.prompts import ChatPromptTemplate

condense_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given the chat history and the latest question, "
               "rewrite it as a standalone question. Do NOT answer it."),
    ("human", "Chat history:\n{chat_history}\n\nQuestion: {question}"),
])

def condense_question(chat_history: str, question: str) -> str:
    """Rewrite follow-up as standalone for retrieval."""
    return (condense_prompt | llm | StrOutputParser()).invoke({
        "chat_history": chat_history,
        "question": question,
    })
```

## Section 8: Multi-tenancy

If multiple orgs or users use the same RAG system, document isolation is critical. A user from Org A must never retrieve documents from Org B.

### Code: Per-tenant collections

```python
def get_vector_store_for_tenant(tenant_id: str):
    """Return a vector store scoped to one tenant."""
    return Chroma(
        client=client,
        collection_name=f"kb_{tenant_id}",
        embedding_function=embeddings,
    )

def ingest_for_tenant(tenant_id: str, docs: list[Document]):
    """Ingest documents into tenant-specific collection."""
    vs = get_vector_store_for_tenant(tenant_id)
    for doc in docs:
        doc.metadata["tenant_id"] = tenant_id
    vs.add_documents(docs)

def retrieve_for_tenant(tenant_id: str, query: str, k: int = 10):
    """Retrieve only from tenant's collection."""
    vs = get_vector_store_for_tenant(tenant_id)
    return vs.similarity_search_with_relevance_scores(query, k=k)
```

### Code: Metadata-filtered multi-tenancy (pgvector)

For large multi-tenant systems, use a single collection with metadata filters instead of per-tenant collections:

```python
from langchain_core.documents import Document
from langchain_postgres import PGVector

def retrieve_with_tenant_filter(query: str, tenant_id: str, k: int = 10):
    """Retrieve with tenant isolation via metadata filter."""
    vector_store = PGVector(
        connection=DATABASE_URL,
        collection_name="knowledge_base",
        embeddings=embeddings,
    )
    return vector_store.similarity_search_with_relevance_scores(
        query=query,
        k=k,
        filter={"tenant_id": tenant_id},
    )
```

### Multi-tenancy rules

- **Small (<50 tenants)**: Per-tenant collections (Chroma). Simple, fast, clean.
- **Medium (50-1000 tenants)**: Per-tenant collections with pgvector schema-per-tenant.
- **Large (1000+ tenants)**: Single collection with metadata filters and tenant_id column.
- **Enterprise**: Row-level security (RLS) in Postgres. The database enforces isolation, not the app.
- **Never**: Trust client-side tenant filtering without database-level enforcement.

## Section 9: FastAPI backend

### Code: Production streaming endpoint

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    conversation_id: str | None = None
    tenant_id: str | None = None

@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """Stream chat response with source documents."""
    async def event_stream():
        # Use tenant-scoped retriever if tenant_id provided
        if req.tenant_id:
            docs = retrieve_for_tenant(req.tenant_id, req.question)
        else:
            docs = retriever.invoke(req.question)

        sources = [
            {
                "doc_id": d.metadata.get("chunk_index"),
                "source_file": d.metadata.get("source_file"),
                "preview": d.page_content[:200],
            }
            for d in docs
        ]
        yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"

        for token in chain.stream(req.question):
            yield f"data: {json.dumps({'type': 'token', 'data': token})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

### Authentication and rate limiting

```python
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from slowapi import Limiter
from slowapi.util import get_remote_address

security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT and return user/tenant info."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=["HS256"],
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/chat/stream")
@limiter.limit("30/minute")
async def chat_stream(
    request: Request,
    req: ChatRequest,
    user: dict = Depends(verify_token),
):
    """Authenticated, rate-limited streaming chat."""
    req.tenant_id = user.get("tenant_id")
    # ... rest of handler
```

## Section 10: Next.js frontend

### Code: Streaming chat UI

```tsx
"use client";
import { useState } from "react";

export default function ChatPage() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);

  async function send() {
    if (!input.trim() || streaming) return;
    setStreaming(true);
    const userMsg = { role: "user", content: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");

    const res = await fetch("http://localhost:8000/api/v1/chat/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ question: input }),
    });

    const reader = res.body!.getReader();
    const decoder = new TextDecoder();
    let assistant = "";
    setMessages((m) => [...m, { role: "assistant", content: "" }]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const lines = decoder.decode(value).split("\n");
      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const { type, data } = JSON.parse(line.slice(6));
        if (type === "token") {
          assistant += data;
          setMessages((m) => {
            const copy = [...m];
            copy[copy.length - 1] = { role: "assistant", content: assistant };
            return copy;
          });
        }
      }
    }
    setStreaming(false);
  }

  return (
    <main className="max-w-2xl mx-auto p-8">
      {messages.map((m, i) => (
        <div key={i} className={m.role === "user" ? "text-right" : ""}>
          {m.content}
        </div>
      ))}
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
        className="border p-2 w-full mt-4"
        placeholder="Ask a question..."
      />
    </main>
  );
}
```

## Section 11: Evaluation

### Rules

- Build a golden test set of 50-100 question-answer pairs BEFORE shipping.
- Measure: context precision, context recall, answer faithfulness, answer relevance.
- Run evals after every change to chunking, embedding, retriever, or LLM.
- Don't ship if any metric drops below 0.7.

### Code: RAGAS evaluation

```python
from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)
from datasets import Dataset

test_cases = [
    {
        "question": "How do I reset my password?",
        "ground_truth": "Go to Settings > Security > Reset Password.",
        "contexts": [...],
        "answer": "...",
    },
]

ds = Dataset.from_list(test_cases)
results = evaluate(
    ds,
    metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
)
print(results)
```

### What to fix based on metrics

| Metric low | What to do |
|---|---|
| Context precision | Better chunking, add reranker, tighten k |
| Context recall | Increase k, add BM25 hybrid, expand chunk size |
| Faithfulness | Lower LLM temperature, add stronger refusal prompt |
| Answer relevancy | Better prompt, give LLM more context chunks |

## Section 12: Observability

### LangSmith setup

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."
os.environ["LANGCHAIN_PROJECT"] = "rag-prod"
```

That's it. LangChain auto-traces every chain call.

### What to track

- Query latency. P50 under 3s, P95 under 8s.
- Token cost per query. Alert above $0.10.
- Retrieval recall (what % of queries get relevant docs in top-k).
- User feedback (thumbs up/down on answers).
- Empty answers (when LLM says "I don't know"). High rate = retrieval problem.

## Section 13: Deployment

### Docker compose

```yaml
version: "3.9"
services:
  api:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - COHERE_API_KEY=${COHERE_API_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/rag
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
    depends_on: [db, redis]

  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: rag
      POSTGRES_PASSWORD: postgres
    volumes: ["pgdata:/var/lib/postgresql/data"]
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  web:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://api:8000
    depends_on: [api]

volumes:
  pgdata:
```

### Deployment targets

| Stack | Best for | Cost |
|---|---|---|
| Vercel (frontend) + Railway (backend) + Neon (pgvector) | Solo/small team | $5-25/mo |
| AWS ECS + RDS | Enterprise | $$$ |
| Self-host VPS | Privacy-sensitive | $5-20/mo |

## Section 14: GraphRAG (knowledge graphs)

GraphRAG combines vector retrieval with knowledge graph traversal. Use it when relationships between entities matter as much as the text itself.

### When to use GraphRAG

- **Multi-entity reasoning**: "Compare our top 3 suppliers by delivery performance"
- **Cross-document relationships**: "Which products are affected by the new regulation?"
- **Hierarchical data**: Org charts, product taxonomies, legal references
- **Temporal queries**: "What changed in our policy since Q3?"

### When NOT to use GraphRAG

- Simple Q&A over flat documents (vector RAG is enough)
- Corpus is small (<100 documents)
- Latency budget is tight (graph traversal adds 200-500ms)
- You cannot afford the indexing complexity

### Code: GraphRAG with Neo4j

```python
from langchain_community.graphs import Neo4jGraph
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain

graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password",
)

# Index entities from documents
def index_entities_to_graph(docs: list[Document]):
    """Extract entities and relationships, store in Neo4j."""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract entities and relationships from the text. "
                   "Return as JSON: {{'entities': [{{'name':..., 'type':...}}], "
                   "'relationships': [{{'source':..., 'target':..., 'type':...}}]}}"),
        ("human", "{text}"),
    ])

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    for doc in docs:
        result = llm.invoke(extract_prompt.format(text=doc.page_content))
        data = eval(result.content)  # Use json.loads in production
        for entity in data.get("entities", []):
            graph.query(
                "MERGE (n:Entity {name: $name, type: $type})",
                params=entity,
            )
        for rel in data.get("relationships", []):
            graph.query(
                """MERGE (a:Entity {name: $source})
                   MERGE (b:Entity {name: $target})
                   MERGE (a)-[:RELATES_TO {type: $type}]->(b)""",
                params=rel,
            )
```

### Hybrid: Vector + Graph

The most powerful pattern. Use vector search for initial retrieval, then expand with graph relationships:

```python
def hybrid_retrieve(query: str, tenant_id: str):
    # Step 1: Vector retrieval for relevant chunks
    vector_docs = retrieve_for_tenant(tenant_id, query, k=5)

    # Step 2: Extract entities from query
    entities = extract_entities(query)

    # Step 3: Graph traversal for related entities
    graph_context = graph.query(
        """MATCH (e:Entity)-[r:RELATES_TO*1..2]-(related)
           WHERE e.name IN $entities
           RETURN e.name, type(r), related.name, related.type
           LIMIT 20""",
        params={"entities": entities},
    )

    # Step 4: Combine context for LLM
    combined_context = format_vector_docs(vector_docs) + "\n\n" + format_graph_context(graph_context)
    return combined_context
```

## Section 15: Document management

### Incremental updates

When a document changes, you must update the vector store without re-embedding everything:

```python
def upsert_document(file_path: str, tenant_id: str):
    """Update or insert a document, removing old chunks first."""
    path = Path(file_path)
    file_hash = hashlib.md5(path.read_bytes()).hexdigest()[:12]

    vs = get_vector_store_for_tenant(tenant_id)

    # Check if document exists with same hash
    existing = vs.get(where={"file_hash": file_hash})
    if existing and len(existing["ids"]) > 0:
        return "No changes detected"

    # Delete old chunks for this file
    old_chunks = vs.get(where={"source_file": path.name})
    if old_chunks and old_chunks["ids"]:
        vs.delete(ids=old_chunks["ids"])

    # Load, chunk, and insert new version
    docs = load_document(file_path)
    chunks = chunk_documents(docs)
    for chunk in chunks:
        chunk.metadata["tenant_id"] = tenant_id
    vs.add_documents(chunks)

    return f"Updated {len(chunks)} chunks for {path.name}"
```

### Document deletion

```python
def delete_document(source_file: str, tenant_id: str):
    """Remove a document and all its chunks from the vector store."""
    vs = get_vector_store_for_tenant(tenant_id)
    chunks = vs.get(where={"source_file": source_file})
    if chunks and chunks["ids"]:
        vs.delete(ids=chunks["ids"])
        return f"Deleted {len(chunks['ids'])} chunks for {source_file}"
    return "Document not found"
```

## Section 16: Anti-patterns

Things that look smart in tutorials but break in production:

1. LLM-as-router: Routing queries to different chains via LLM decision. Adds latency and fails silently. Use rules.
2. Multi-hop retrieval: LLM decides to retrieve again. Costs explode, quality drops. Use better chunking.
3. Massive context windows: Stuffing 100k tokens into Claude. Slower, more expensive, often worse retrieval. Use smaller chunks + reranking.
4. Auto-generated summaries as embeddings: Sounds clever, loses detail. Embed the actual chunk.
5. No evaluation set: You will never know if changes help or hurt.
6. Fine-tuning embeddings on small data: Need 10k+ examples to help. Below that, wasted effort.
7. Caching at wrong layer: Cache embeddings, not LLM responses (unless queries repeat exactly).
8. Sync ingestion in the request path: Ingest documents async via background jobs.
9. No multi-tenancy isolation: A bug that can cost you the entire business. One lawsuit and you're done.
10. Storing all history in memory: OOM crashes. Use Redis or database-backed memory with TTL.
11. No document lifecycle management: Documents get stale. Have an update and deletion strategy.

## Section 17: Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Low faithfulness score | LLM hallucinating beyond context | Lower temperature, strengthen refusal prompt |
| Low context recall | Retrieval missing relevant docs | Add BM25 hybrid, increase k, tune chunk size |
| High "I don't know" rate | Retriever not finding docs | Check embeddings, add HyDE query rewriting |
| Slow query latency | Large k, no reranker caching | Reduce k to 5, add reranker top_n=4, cache embeddings |
| Streaming not working | FastAPI not async or middleware blocking | Use `StreamingResponse` with `text/event-stream` |
| Cross-tenant data leak | Metadata filter not applied | Use per-tenant collections or RLS in Postgres |
| Memory OOM | Conversation history growing unbounded | Use Redis memory with TTL=3600 |
| Cost spikes | GPT-4o instead of GPT-4o-mini | Audit model usage, use mini for chat, 4o for evals only |

## Section 18: Project structure

```
rag-app/
- backend/
  - app/
    - api/v1/
      - chat.py
      - documents.py
      - auth.py
    - services/
      - rag_service.py
      - ingest_service.py
      - graph_service.py
    - core/
      - config.py
      - security.py
    - main.py
  - tests/
  - requirements.txt
  - Dockerfile
- frontend/
  - src/app/
  - package.json
  - Dockerfile
- evals/
  - golden_set.json
  - run_evals.py
- docker-compose.yml
- README.md
```

## Section 19: Pricing for client work (2026)

Real ranges from freelance and agency work:

| Project type | Price range (USD) |
|---|---|
| Basic RAG chatbot (1 source, no reranker) | $2,000-5,000 |
| Production RAG (reranker, evals, hybrid search) | $8,000-20,000 |
| Multi-tenant RAG (auth, per-org collections) | $15,000-35,000 |
| GraphRAG (Neo4j + vector hybrid) | $20,000-50,000 |
| Enterprise RAG (SSO, audit log, SLAs, multi-region) | $25,000-100,000 |
| Monthly maintenance + improvements | $500-3,000/mo |

## Section 20: Reference workflow

When a user says "build me a RAG chatbot", follow this order:

1. Scope: What corpus? How many docs? How fast does it change?
2. Stack selection: Default stack unless special requirements.
3. Loader + chunker: Build ingestion pipeline. Test on 5-10 sample docs.
4. Vector store + retriever: Chroma for dev, pgvector for prod.
5. Streaming chat: Get a working end-to-end chat first.
6. Golden set: Build 50 test questions with the client.
7. Add reranker + hybrid search: Measure improvement on golden set.
8. Conversation memory: Add Redis-backed memory for multi-turn.
9. Multi-tenancy: If B2B, add tenant isolation now, not later.
10. Auth + rate limiting: JWT auth, per-user limits.
11. Eval suite: RAGAS or custom. Set thresholds.
12. Observability: LangSmith traces.
13. Deploy + monitor: First week, watch every query.

## Closing notes

- RAG is not "embeddings + LLM". It is a system. Treat it like one.
- The retriever is 70% of the quality. Spend most of your time there.
- If you cannot show evals, you cannot call it production-ready.
- Streaming is non-negotiable for UX.
- Source citations are non-negotiable for trust.
- Multi-tenancy isolation is non-negotiable for B2B. One leak can kill the company.

## Related skills

- **business-data-automator**: For dashboard and automation work (no LLM)
- **ml-pipeline-builder**: For traditional ML pipelines (classification, forecasting)
# Literature Agent – Future Architecture Notes

This document tracks architectural improvements that should be implemented
after the initial working system is complete.

The goal is to allow rapid prototype development while preserving a clear
path toward a scalable research intelligence platform.

---

# 1. Agent Execution Model

Current implementation:

Agents run as **threads inside a single Python process**.

Reason:
- Faster development
- Simpler debugging
- No IPC complexity

Future architecture:

Agents should run as **separate processes or services**.

Benefits:

- Horizontal scalability
- Fault isolation
- Independent deployment
- Better resource management (GPU / CPU agents)

Possible approaches:

Option A
- Python multiprocessing
- Shared database queues

Option B
- Containerized agents
- Message broker (Redis / RabbitMQ)

Option C
- Kubernetes style worker agents

Transition trigger:

When:
- ingestion rate increases
- embedding workloads become GPU heavy
- reasoning agents become slow

---

# 2. Queue Backend

Current:

In-memory Python queues.

Future:

Move to **database-backed queues**.

Preferred options:

- PostgreSQL queue tables
- Redis streams
- RabbitMQ

Reason:

- persistence
- crash recovery
- distributed workers

---

# 3. Event Router

Current:

Simple in-process router.

Future:

Event router should become a **publish/subscribe event bus**.

Possible implementation:

- Redis PubSub
- Kafka
- PostgreSQL LISTEN/NOTIFY

---

# 4. Embedding Storage

Current:

Embeddings stored locally.

Future:

Vector database integration:

Options:

- pgvector
- Qdrant
- Weaviate
- Milvus

---

# 5. Reasoning Agents

Future reasoning agents may include:

- literature summarization
- research gap detection
- experiment suggestion
- project relevance updates
- novelty detection

---

# 6. Autonomous Literature Discovery

Future agents should:

- monitor arXiv
- monitor journals
- monitor citation networks
- perform topic exploration

This enables **true continuous scientific monitoring**.

---

# 7. Spine Integration

Eventually the Literature Agent becomes **one subsystem inside Spine**.

Integration points:

Spine → Literature Agent

- new project created
- project description updated
- research query

Literature Agent → Spine

- relevant paper notifications
- domain summaries
- research insights

---

# Philosophy

Prototype quickly.

Preserve architectural clarity.

Scale later without rewriting the system.
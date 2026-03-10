# Embedding Agent Layer Plan

## Purpose

Introduce an embedding layer into the literature ingestion pipeline to enable semantic filtering before LLM reasoning. The system should remain modular so that embedding models, similarity logic, and reasoning agents can evolve independently.

---

# 1. Agent Responsibilities

The embedding layer will consist of two agents:

1. **Embedding Agent**
2. **Similarity Screening Agent**

This separation allows embeddings to be reused for future capabilities such as:

* vector search
* clustering
* hierarchical knowledge structures

---

# 2. System Pipeline

Updated literature processing pipeline:

```
paper_source
→ ingestion_engine
→ embedding_agent
→ similarity_queue
→ similarity_screening_agent
→ reasoning_queue
→ reasoning_agents
```

This architecture uses event-driven queues between agents so that each stage can operate independently and scale if needed.

---

# 3. Embedding Agent

## Responsibilities

The embedding agent is responsible for:

* generating embeddings for papers
* storing embeddings in the embedding database
* preventing duplicate embedding generation
* pushing newly embedded papers to the similarity screening queue

The embedding agent **does not perform similarity comparisons**.

---

## Input

Paper object:

```
paper_id
title
abstract
source
```

---

## Processing

Create text for embedding:

```
title + abstract
```

Generate embedding vector using the configured embedding model.

---

## Storage

Paper metadata and embeddings are stored separately.

### Paper Table

```
papers
------
paper_id
title
abstract
source
date_ingested
```

### Embedding Table

```
embeddings
----------
paper_id
embedding_vector
embedding_model
created_at
```

This separation allows embeddings to be regenerated if embedding models change.

---

## Important Rule

A paper should only be embedded **once per embedding model**.

Before generating an embedding:

```
check if paper_id already exists in embeddings table
```

If it exists, skip embedding generation.

---

## Queue Integration

After storing the embedding, the embedding agent pushes a message to the similarity queue.

Queue message format:

```
paper_id
```

Only the paper identifier is pushed to the queue.

The similarity agent retrieves the full embedding and paper metadata from the database when processing.

This keeps queue messages lightweight and avoids large vector transfers between agents.

---

# 4. Similarity Screening Agent

## Purpose

Evaluate whether a paper should be passed to reasoning agents based on semantic similarity to project topics.

---

## Input

Queue message:

```
paper_id
```

The similarity agent retrieves the paper embedding and metadata from the database.

---

# 5. Project Definitions

Projects contain a set of semantic topics.

Example project:

```
project_id
topics:
• CO₂ capture materials
• 3D printed porous structures
• CFD airflow modelling
```

Each topic contains:

```
topic_text
topic_embedding
high_threshold
low_threshold
```

---

# 6. Similarity Processing

For each project and each topic:

```
similarity = cosine_similarity(paper_embedding, topic_embedding)
```

This produces a similarity score for each topic.

A paper may match **multiple projects or topics**.

---

# 7. Decision Logic

Three possible outcomes exist.

---

## 1. Immediate Reasoning

If similarity exceeds the **high threshold**:

```
paper → reasoning_queue
```

Queue entry:

```
paper_id
project_id
matched_topic
similarity_score
```

---

## 2. Review Buffer

If similarity falls within the **low threshold range**:

```
low_threshold < similarity < high_threshold
```

The paper is stored in a review buffer.

Review buffer table:

```
review_buffer
-------------
paper_id
project_id
topic_id
similarity_score
recorded_at
```

These papers are periodically sampled by the reasoning agent to:

* adjust thresholds
* refine topic wording
* add new project topics

---

## 3. No Action

If similarity is **below the low threshold**:

The paper is ignored for the current project.

The embedding remains stored for future projects.

---

# 8. Reasoning Queue

Papers that pass the similarity screen are placed in a queue for reasoning agents.

This queue allows reasoning agents to run independently and potentially in parallel.

Queue entry example:

```
paper_id
project_id
matched_topic
similarity_score
```

---

# 9. Reasoning Agent Role

The reasoning agent evaluates papers and produces structured explanations.

Example outputs:

* relevant to CO₂ capture materials
* relevant 3D printing method
* relevant CFD modelling technique

The reasoning agent identifies which aspect of the project the paper contributes to.

---

## System Improvement Role

The reasoning agent can recommend improvements to the similarity system.

Possible suggestions include:

* adjusting topic thresholds
* refining topic descriptions
* adding additional project topics

In early system versions these changes may require human approval.

---

# 10. Data Stores

The embedding system will maintain the following data structures.

### Paper Database

```
papers
------
paper_id
title
abstract
source
date_ingested
```

---

### Embedding Database

```
embeddings
----------
paper_id
embedding_vector
embedding_model
created_at
```

---

### Project Topic Database

```
project_topics
--------------
project_id
topic_text
topic_embedding
high_threshold
low_threshold
```

---

### Similarity Records (optional)

```
similarity_records
------------------
paper_id
project_id
topic_scores
```

These records enable later analysis and threshold tuning.

---

# 11. Incremental Implementation

## Step 1

Create embedding agent.

Capabilities:

* generate embeddings
* store embeddings
* push paper IDs to similarity queue

---

## Step 2

Create similarity screening agent.

Capabilities:

* consume similarity queue
* compute similarity
* route papers to reasoning queue

---

## Step 3

Integrate reasoning queue.

Papers passing similarity thresholds are processed by reasoning agents.

---

# 12. Future Extensions

The architecture supports later development of:

* hierarchical embeddings
* topic clustering
* automated topic discovery
* semantic literature mapping
* project knowledge graphs

Because embeddings are stored independently, these capabilities can be added without changing the ingestion pipeline.

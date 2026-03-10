# Literature Intelligence System – Data Models

This document defines the core data structures used by the literature ingestion and reasoning pipeline.

These models describe the objects exchanged between agents and stored in the system's databases.

---

# 1. Paper Object

The **Paper** object represents a scientific publication as it moves through the pipeline.

It is produced by the ingestion agent and passed between agents.

## Paper Schema

```id="p9x5xn"
Paper {
    paper_id: string,
    title: string,
    abstract: string,
    source: string,
    authors: [string] | null,
    publication_date: string | null,
    date_ingested: string,
}
```

### Notes

* `paper_id` should uniquely identify the paper.
* Suggested formats:

  * arxiv: `arxiv:2401.12345`
  * doi: `doi:10.1038/example`
* The paper object **does not contain embeddings**. Embeddings are stored separately.

---

# 2. Embedding Record

Embeddings are stored separately from the paper record so they can be regenerated or replaced if embedding models change.

## Embedding Schema

```id="f7clo0"
EmbeddingRecord {
    paper_id: string,
    embedding_vector: [float],
    embedding_model: string,
    embedding_created: timestamp
}
```

### Notes

* A paper may have multiple embeddings if the embedding model changes in the future.
* Current system will generate **one embedding per paper**.

---

# 3. Project

A **Project** represents a research program that the system tracks for relevant literature.

Projects contain one or more semantic topics.

## Project Schema

```id="c1kfrb"
Project {
    project_id: string,
    name: string,
    description: string,
    created_at: timestamp
}
```

---

# 4. Project Topic

Projects are broken into **semantic topics** that allow fine-grained literature matching.

## Topic Schema

```id="37ixs9"
ProjectTopic {
    topic_id: string,
    project_id: string,
    topic_text: string,
    topic_embedding: [float],
    high_threshold: float,
    low_threshold: float,
    created_at: timestamp
}
```

### Example

Topic text:

```id="h7a3q8"
"3D printed porous structures for CO2 capture"
```

Each topic is embedded and compared to paper embeddings.

---

# 5. Similarity Record

Similarity records track the semantic similarity between papers and project topics.

These records allow later analysis of threshold performance and embedding quality.

## Similarity Schema

```id="p6iyv0"
SimilarityRecord {
    paper_id: string,
    project_id: string,
    topic_id: string,
    similarity_score: float,
    timestamp: timestamp
}
```

---

# 6. Similarity Queue Message

The similarity queue connects the embedding agent and the similarity screening agent.

Queue messages are intentionally minimal.

## Queue Schema

```id="1zq3jv"
SimilarityQueueMessage {
    paper_id: string
}
```

The similarity agent retrieves the embedding and paper metadata from the database.

---

# 7. Reasoning Queue Message

Papers that pass similarity thresholds are passed to reasoning agents.

## Queue Schema

```id="v9v0fh"
ReasoningQueueMessage {
    paper_id: string,
    project_id: string,
    topic_id: string,
    similarity_score: float
}
```

This provides the reasoning agent with context for evaluating the paper.

---

# 8. Review Buffer Record

Papers within the low similarity threshold band are stored for periodic evaluation.

## Review Schema

```id="7c6xx5"
ReviewBufferRecord {
    paper_id: string,
    project_id: string,
    topic_id: string,
    similarity_score: float,
    recorded_at: timestamp
}
```

These records are periodically sampled to improve topic definitions and thresholds.

---

# 9. Future Extensions

The current models support several future capabilities.

Possible future objects include:

### Topic Cluster

Grouping semantically related topics.

### Knowledge Graph Node

Representing relationships between:

* papers
* methods
* materials
* datasets

### Domain Hierarchy

Supporting hierarchical embeddings such as:

```id="h9o4k0"
domain
   → topic
       → subtopic
           → paper
```

These capabilities can be introduced without changing the existing core pipeline.

---

# 10. Design Principles

The data model follows several guiding principles.

**Separation of concerns**

Papers, embeddings, and similarity records are stored separately.

**Agent modularity**

Each agent operates on well-defined objects.

**Persistent semantic memory**

Embeddings are stored permanently to support historical retrieval.

**Future extensibility**

The models support hierarchical knowledge and advanced literature intelligence features.

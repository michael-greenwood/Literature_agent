# Literature Intelligence System – Architecture Plan

## Literature Ingestion and Relevance System

### Incremental Architecture Plan

---

# 1. System Goal

Build a persistent literature ingestion and reasoning system that:

* continuously ingests scientific papers
* evaluates relevance to active research projects
* stores semantic embeddings for long-term retrieval
* improves retrieval quality through adaptive feedback

The system is intentionally built incrementally so it can evolve into a larger **research intelligence platform** supporting:

* hierarchical embeddings
* agent-driven topic expansion
* adaptive similarity thresholds
* persistent literature knowledge bases

---

# 2. Core Pipeline

The system processes literature through a staged agent pipeline.

```
paper_source
    ↓
ingestion_agent
    ↓
embedding_agent
    ↓
similarity_queue
    ↓
similarity_screening_agent
    ↓
reasoning_queue
    ↓
reasoning_agent
    ↓
storage
```

Agents communicate through **queues**, allowing components to operate independently and scale if necessary.

Key principle:

**Each paper is embedded once during ingestion.**

---

# 3. Paper Embedding Strategy

## Initial Implementation

Each paper receives a **single embedding** created from:

```
title + abstract
```

This provides strong semantic representation while keeping the system simple.

---

## Future Expansion (Supported but Not Required Initially)

The system may later support **multiple embeddings per paper**, for example:

* title embedding
* abstract embedding
* keywords embedding
* section embeddings

This allows more granular semantic matching but will not be used initially to avoid unnecessary redundancy and complexity.

---

# 4. Project Representation

Each project is represented as a **set of semantic topics**.

Example project:

Project: **CCUS Printed Structures**

Topics:

* CO₂ capture materials
* 3D printed porous structures
* CFD airflow modelling
* adsorption coatings

Each topic receives its own embedding.

Similarity is calculated between:

```
paper_embedding
      and
each_project_topic_embedding
```

---

# 5. Similarity Filtering Strategy

Embedding similarity acts as a **pre-filter**, not a final decision.

Two thresholds are used.

---

## High Threshold (Immediate Review)

If similarity exceeds the high threshold:

```
paper → reasoning_agent
```

Example:

```
similarity > 0.70
```

These are likely relevant papers.

---

## Low Threshold Range (Periodic Review)

Papers falling into a lower similarity band are stored for periodic review.

Example:

```
0.45 < similarity < 0.70
```

These papers are not immediately processed but are periodically sampled by the reasoning agent to determine:

* whether the threshold should be adjusted
* whether topic wording should be improved
* whether additional topic embeddings should be added

This creates a **self-improving retrieval system**.

---

# 6. Role of the Reasoning Agent

The reasoning agent performs **semantic interpretation**, not just classification.

Its responsibilities include:

---

## 1. Relevance Determination

Confirm whether a paper is relevant to a project.

---

## 2. Explanation of Relevance

Provide structured reasoning describing:

* **why the paper is relevant**
* **which project aspect it relates to**

Example outputs:

* relevant to CO₂ capture materials
* relevant printing method for porous lattices
* relevant modelling technique for airflow analysis

This produces structured explanations similar to the original demo system.

---

## 3. Retrieval System Improvement

The reasoning agent can also suggest improvements to the embedding retrieval system.

Examples:

* lowering or raising topic thresholds
* refining topic descriptions
* adding additional project topics

Early versions may require **human approval** for these changes.

---

# 7. Embedding Agent Responsibilities

The embedding agent manages the **semantic representation layer**.

Responsibilities:

* generate embeddings for papers
* store embeddings for long-term retrieval
* generate embeddings for project topics
* push paper identifiers to the similarity queue

The embedding agent **does not perform similarity comparisons**.

Similarity evaluation is handled by the **similarity screening agent**.

---

# 8. Similarity Screening Agent

The similarity screening agent evaluates whether papers should be passed to reasoning agents.

Responsibilities:

* consume paper identifiers from the similarity queue
* retrieve embeddings from the embedding database
* compare paper embeddings with project topic embeddings
* apply similarity thresholds
* route papers to reasoning or review buffers

Decision outcomes:

```
similarity ≥ high_threshold
    → reasoning_queue

low_threshold ≤ similarity < high_threshold
    → review_buffer

similarity < low_threshold
    → ignore
```

---

# 9. Storage Strategy

The system stores several core objects.

---

## Paper Record

```
paper_id
title
abstract
source
date_ingested
embedding_vector
```

---

## Project Topics

```
project_id
topic_text
topic_embedding
threshold
```

---

## Similarity Records (Recommended)

```
paper_id
project_id
topic_id
similarity_score
timestamp
```

These records allow later tuning of similarity thresholds and evaluation of embedding performance.

---

# 10. Embedding Database

Embeddings are stored persistently to support future retrieval.

This enables two operational modes.

---

## Streaming Mode (Primary)

New papers are embedded and immediately compared against active projects.

```
paper → embed → compare → filter
```

---

## Historical Search Mode

When a new project is created:

```
project → embed topics → query embedding database → retrieve historical papers
```

This allows the system to reason over previously ingested literature.

---

# 11. Incremental Development Plan

## Phase 1 (Current)

* paper ingestion
* single paper embedding
* project topic embeddings
* similarity filtering
* reasoning explanation

---

## Phase 2

* adaptive threshold tuning
* periodic low-similarity review
* topic wording refinement

---

## Phase 3

* automatic topic suggestions
* project semantic expansion

---

## Phase 4

* hierarchical embedding structures

Example hierarchy:

```
domain
  → topic
    → subtopic
      → paper
```

---

# 12. Long-Term Vision

The architecture evolves into a persistent **research intelligence system** capable of:

* continuous literature monitoring
* semantic project tracking
* adaptive knowledge expansion
* automated detection of emerging research directions

Rather than functioning as a static literature search tool, the system becomes a **closed-loop literature reasoning engine** that improves its understanding of research domains over time.

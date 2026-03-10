# Agent Architecture

## Overview

The literature intelligence system is built around **specialized agents** that each perform a focused task within the pipeline.

Agents communicate through queues and shared data stores.

This modular design allows agents to be developed, replaced, or scaled independently.

---

# Current Agents

## Ingestion Engine

Loads papers from external sources and converts them into normalized paper objects.

Inputs:

paper sources (JSON or APIs)

Outputs:

paper objects passed to the embedding agent.

---

## Embedding Agent

Generates semantic embeddings for papers.

Responsibilities:

* create embedding vectors
* store embeddings in the embedding database
* push paper identifiers to the similarity queue

Embeddings are created from:

title + abstract

Future versions may support multiple embeddings per paper.

---

## Similarity Screening Agent

Evaluates whether papers should be passed to reasoning agents.

The agent compares paper embeddings with project topic embeddings.

Possible outcomes:

Immediate reasoning
Paper exceeds high similarity threshold.

Review buffer
Paper falls within low similarity band.

No action
Paper similarity is below low threshold.

---

## Reasoning Agents

Reasoning agents perform semantic analysis of candidate papers.

Outputs include:

* relevance determination
* explanation of relevance
* identification of relevant project topics

Example outputs:

Relevant CO₂ capture material

Relevant 3D printing method

Relevant CFD modelling technique

---

# Adaptive System Behavior

Reasoning agents may suggest improvements to the similarity system.

Examples:

Adjust topic thresholds

Refine topic wording

Add new project topics

In early versions these updates may require human approval.

---

# Future Agents

The architecture supports additional agents in later phases.

Topic discovery agents
Identify new research areas emerging in the literature.

Trend analysis agents
Track developments across research fields.

Knowledge graph agents
Construct semantic relationships between papers, materials, and methods.

Autonomous monitoring agents
Continuously search for new research relevant to active projects.

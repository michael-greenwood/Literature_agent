# Literature Intelligence Agent

### (Spine Subsystem: Literature Scrape & Triage Engine)

------------------------------------------------------------------------

## Overview

The **Literature Intelligence Agent** is an AI-driven literature
ingestion and triage system designed to continuously monitor scientific
abstracts and route them to relevant research projects.

This module serves as a prototype component of the broader **Spine
Research Intelligence Platform**, where it will eventually operate as a
persistent, autonomous knowledge-building agent.

This demo version focuses on:

-   Continuous abstract ingestion
-   Structured LLM-based decomposition
-   Project-level relevance scoring
-   Automated routing and discard logic
-   Live monitoring through a frontend dashboard

------------------------------------------------------------------------

## What This Demo Demonstrates

This is **not** a chatbot.

It is a structured AI reasoning system that:

1.  Ingests abstracts
2.  Extracts structured scientific elements:
    -   Problem
    -   Materials
    -   Methods
    -   Findings
    -   Limitations
3.  Evaluates each paper against active project definitions
4.  Assigns:
    -   Relevance score
    -   Include / Watch / Exclude recommendation
    -   Confidence
    -   Explicit reasoning signals
5.  Routes papers into project buckets or discards them

The system maintains a live in-memory state to simulate continuous
ingestion.

------------------------------------------------------------------------

## Architecture

### Backend (FastAPI + Python)

-   `engine.py` -- Core ingestion loop and routing logic
-   `llm_client.py` -- LLM query interface
-   `prompt_loader.py` -- Externalized prompt templates
-   `models.py` -- Memory structure
-   `data_loader.py` -- Demo corpus loader
-   `api.py` -- REST interface for frontend interaction

The engine runs in a background thread and maintains structured memory.

### Frontend (React + MUI)

-   Dashboard with:
    -   Engine controls (Start / Reset)
    -   Live processing status
    -   Project summaries
    -   Recent activity feed
-   Project Detail view
-   Papers table view
-   Paper Detail view with full AI reasoning

------------------------------------------------------------------------

## API Endpoints

  Endpoint          Method   Description
  ----------------- -------- --------------------------
  `/engine/start`   POST     Start ingestion
  `/engine/reset`   POST     Reset memory
  `/engine/state`   GET      Return full engine state

------------------------------------------------------------------------

## Running the Demo

### Backend

Activate virtual environment:

    source .venv/bin/activate

Run:

    uvicorn api:app --reload --host 0.0.0.0 --port 8001

------------------------------------------------------------------------

### Frontend

From `spine/` directory:

    npm run dev -- --host

Open:

    http://<machine-ip>:5173

------------------------------------------------------------------------

## Demo Data

This repository includes small demo datasets:

-   `abstracts.json`
-   `projects.json`

These are intentionally lightweight and committed to the repo for
reproducibility.

Runtime memory state is not persisted.

------------------------------------------------------------------------

## Design Philosophy

This agent is intentionally designed to:

-   Be structured, not conversational
-   Produce machine-usable reasoning artifacts
-   Make explicit scoring decisions
-   Separate extraction from scoring
-   Allow deterministic routing rules

It is a building block toward a larger system featuring:

-   Persistent domain memory
-   Vector embeddings
-   Multi-agent orchestration
-   Continuous literature monitoring
-   Strategic objective alignment

------------------------------------------------------------------------

## Future Extensions

Planned evolution within Spine:

-   Persistent database storage
-   Vector similarity search
-   Lab-level strategic scoring
-   Cross-project signal discovery
-   Relevance drift monitoring
-   Active learning feedback loops
-   Multi-agent literature decomposition

------------------------------------------------------------------------

## Repository Notes

Include: - Demo datasets - Prompt templates - Engine logic

Exclude: - `.venv` - `node_modules` - Runtime logs - Large scraped
corpora

------------------------------------------------------------------------

## Status

This is an early-stage prototype demonstrating:

**AI-driven structured literature triage.**

It will eventually become one autonomous agent within the broader Spine
Research Intelligence Platform.

------------------------------------------------------------------------

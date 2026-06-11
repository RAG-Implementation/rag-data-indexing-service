# docs

Project documentation and design references. This directory holds documents that explain the goals, architecture, and decisions behind the project — things that do not belong in code comments or README files for individual folders.

## Table of Contents

- [1. Files](#1-files)
  - [1.1. Project_Goal.md](#11-project_goalmd)
  - [1.2. Implementation_Plan.md](#12-implementation_planmd)
- [2. When to Add to This Directory](#2-when-to-add-to-this-directory)

## 1. Files

| File | Purpose |
|---|---|
| `Project_Goal.md` | Full project specification: goals, pipeline stages, technology stack, API design, success criteria, and the design rationale behind every major decision. This is the authoritative reference for what the project is supposed to do and why. |
| `Implementation_Plan.md` | Step-by-step execution plan for building the project in two stages: notebooks (Phases 1-7) and the production service layer (Phases 8-11). Includes the phase map, data flow, per-phase cell breakdowns, and key architectural decisions. |

### 1.1. Project_Goal.md

A complete written spec for the `rag-data-indexing-service`. It covers:

- The problem this project solves (data preparation for RAG, not retrieval or generation).
- Each pipeline stage in detail: document loading, text cleaning, chunking strategies, metadata enrichment, embedding generation, and Qdrant indexing.
- Technology stack choices with rationale (Python 3.11+, FastAPI, Typer, Qdrant, sentence-transformers, LangChain splitters, structlog, pytest, ruff, black, Docker).
- API endpoints with example request/response shapes.
- CLI commands.
- What the project intentionally does not do (no LLM, no hybrid retrieval, no reranking).
- Success criteria that define when the project is complete.

### 1.2. Implementation_Plan.md

The step-by-step execution strategy for building the project. It covers:

- A two-stage approach: notebooks first (to validate logic interactively), service layer second (to package and test that logic for production).
- The notebook house style that every notebook must follow: `<div>` title, numbered sections, step marker comments, configuration cell, and a final verification cell.
- A phase map table showing all 11 phases with their associated notebooks or modules and current status.
- The full data flow from `data/raw/corpus/corpus.jsonl` through each `data/processed/` file to the Qdrant collection.
- Per-phase breakdowns listing every numbered cell or module that must be implemented.
- Key architectural decisions with rationale (notebook numbering, read-chain design, reuse over rewrite, `data/processed/` convention).

## 2. When to Add to This Directory

Add a document here when:

- It explains a design decision that spans multiple modules (e.g., why a particular chunking strategy was chosen as the default).
- It describes the roadmap or planned extensions to the project.
- It is reference material that a new contributor needs to read before touching the code.

Do not add auto-generated API docs here. FastAPI generates those at runtime at `http://localhost:8000/docs`.

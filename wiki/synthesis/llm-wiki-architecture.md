---
title: "LLM Wiki Architecture"
type: synthesis
created: 2026-08-23
updated: 2026-08-23
tags:
  - architecture
  - system-design
  - llm-agents
aliases:
  - Second Brain Architecture
sources:
  - "[[wiki/sources/llm-wiki-idea|LLM Wiki Idea Manifest]]"
---

# LLM Wiki Architecture

A structural overview of the 3-layer architecture for personal second brains maintained by autonomous LLM agents.

---

## Structural Layers

```text
+-------------------------------------------------------------+
| 1. RAW LAYER (raw/)                                         |
|    Immutable source documents, web clippings, assets, PDFs  |
+-------------------------------------------------------------+
                              │ (Ingested by LLM)
                              ▼
+-------------------------------------------------------------+
| 2. WIKI LAYER (wiki/)                                       |
|    • Sources      • Concepts    • Entities                  |
|    • Synthesis    • Comparisons                             |
+-------------------------------------------------------------+
                              ▲
                              │ (Governed & Indexed by)
+-------------------------------------------------------------+
| 3. CONTROL LAYER (CLAUDE.md, index.md, log.md)              |
|    Operational rules, topic catalog, chronological log      |
+-------------------------------------------------------------+
```

## Core Operations
1. **`ingest`**: Reads raw source, creates breakdown, updates affected concepts/entities, updates `index.md` & `log.md`.
2. **`query`**: Reads compiled wiki pages to answer deep questions, saving high-value answers back into `wiki/synthesis/`.
3. **`lint`**: Audits link integrity, checks for orphans, identifies contradictions, surfaces knowledge gaps.

## Related Links
- **[[wiki/concepts/compounding-knowledge|Compounding Knowledge]]**
- **[[wiki/comparisons/rag-vs-llm-wiki|RAG vs. LLM Wiki]]**
- **[[wiki/entities/obsidian|Obsidian]]**

---
title: "RAG vs. LLM Wiki"
type: comparison
created: 2026-08-23
updated: 2026-08-23
tags:
  - comparison
  - rag
  - pkm
aliases:
  - RAG Comparison
sources:
  - "[[wiki/sources/llm-wiki-idea|LLM Wiki Idea Manifest]]"
---

# Comparison: Stateless RAG vs. Compounding LLM Wiki

A comparative breakdown between naive retrieval-augmented generation and a persistent LLM-maintained wiki.

---

| Dimension | Standard RAG | LLM Wiki Pattern |
| :--- | :--- | :--- |
| **Statefulness** | Stateless per session / per query | Persistent, version-controlled markdown repo |
| **Knowledge Assembly** | Ephemeral chunk retrieval on query | Pre-compiled, continuously integrated synthesis |
| **Cross-Referencing** | Implicit / stochastic | Explicit, human-readable Obsidian wikilinks |
| **Multi-Source Synthesis** | High latency, loses subtle threads | Compounded over time across dozens of documents |
| **Contradiction Detection** | Often confused by conflicting chunks | Explicitly flagged and reconciled in synthesis pages |
| **Human Role** | Prompt engineer & chunk reviewer | Curator of sources, explorer, director |
| **LLM Role** | Answering machine | Dedicated knowledge base maintainer / gardener |

## Related Links
- **[[wiki/synthesis/llm-wiki-architecture|LLM Wiki Architecture]]**
- **[[wiki/concepts/compounding-knowledge|Compounding Knowledge]]**

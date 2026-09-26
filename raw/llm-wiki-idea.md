# LLM Wiki: A pattern for building personal knowledge bases using LLMs

The core idea: Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files that sits between you and the raw sources.

Architecture:
1. Raw sources — immutable source of truth.
2. The wiki — directory of LLM-generated markdown files (summaries, entity pages, concept pages, comparisons, overview, synthesis).
3. The schema — document (e.g. CLAUDE.md) defining structure and workflows.

Operations:
- Ingest: Process new sources, update 10-15 wiki pages, update index and log.
- Query: Ask questions against the wiki, file valuable syntheses back as new pages.
- Lint: Health-check for contradictions, stale claims, orphan pages, missing cross-references.

Key insight: The wiki is a persistent, compounding artifact. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

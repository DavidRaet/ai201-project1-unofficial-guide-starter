# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A **starter scaffold** for AI201 Project 1, "The Unofficial Guide" — a RAG system answering
student-sourced questions about 7 specific Vassar CS courses and their professors. As of now the
repo contains **only documentation and config, no pipeline code** — the implementation is built
from the spec by the student (directing AI tools). When writing code, you are implementing the
five-stage RAG pipeline described in the PRD, not modifying an existing one.

## Source of truth (read these first)

- `planning.md` — student-authored design doc that **must be filled in before pipeline code is
  committed** (it's a graded deliverable and the spec the student uses to direct AI tools).
- `README.md` — the graded write-up (domain, sample chunks, retrieval examples, evaluation report,
  failure-case analysis, AI-usage transparency). Sections are filled in *after* each part works.

## Pipeline architecture (five stages)

`Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Grounded Generation`

Per the PRD, the intended stack is:

| Stage | Tool |
|---|---|
| Embeddings | `sentence-transformers` / `all-MiniLM-L6-v2` (local, no API key) |
| Vector store | ChromaDB, local + persistent (`chroma_db/`, gitignored) |
| LLM | Groq `llama-3.3-70b-versatile` (free tier, needs `GROQ_API_KEY`) |
| Backend | Python |
| Frontend | gradio |


## Hard constraints (enforce in any generated code)

- **Grounding is the whole point.** Generation must use *only* retrieved chunks — never the
  model's general knowledge about courses/professors.
- **Exact refusal string** when no relevant context is retrieved:
  `"I don't have enough student-sourced information to answer that question reliably."`
- **Every response** carries inline source citations plus an end-of-response source list.
- **Per-document metadata schema** (attach at ingestion): `source` (one of `rmp`, `reddit`,
  `miscellany`, `syllabus`, `official`), `professor_name`, `course_code`, `raw_url`,
  `approximate_year`.
- **Chunking:** 200–300 tokens, 30–50 token overlap, sentence-aware splitter (no mid-sentence
  splits), prefer paragraph/review boundaries.
- **Scope is exactly the 7 courses/professors in the PRD table.** Anything else (other courses,
  non-CS, housing/dining/campus life) is out of scope and should trigger refusal.
- **Documents must be real student-generated content** (RMP, r/vassar, Miscellany News, syllabi,
  official pages) — no synthetic data. Place them under `documents/`.

## Environment

- Python project. Secrets come from `.env` (gitignored); copy `.env.example` and set `GROQ_API_KEY`.
- `.claude/settings.json` denies reading `.env` — do not attempt to read it; ask the user if a key
  value is needed.
- Install deps: `pip install -r requirements.txt`. Uncomment the Gradio/Streamlit and `pdfplumber`
  lines in `requirements.txt` only if those paths are chosen. 
- No build/lint/test config exists yet; add one alongside the first code rather than assuming one.

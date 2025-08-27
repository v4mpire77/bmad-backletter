# 1) Summary

* **Goal**: Evidence-first GDPR Art. 28(3) checker.
* **Pattern**: Thin **FastAPI** service with modular services: extraction → detection → reporting.
* **Non-goals (MVP)**: OCR by default, RAG, multi-tenant auth beyond org-level settings.

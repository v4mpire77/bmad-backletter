# 2) Architecture Principles

* **Determinism first** (rules-first, LLM optional and off by default).
* **Explainability** (every finding cites a snippet + offsets).
* **Small vertical slices** (one story per PR).
* **Zero trust in inputs** (strict validation, MIME/size checks).
* **Pins & reproducibility** (version-locked dependencies per sprint).

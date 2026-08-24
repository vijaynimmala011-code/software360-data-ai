# Package boundaries

These boundaries keep each layer independently testable, reusable, and
deployable. Code should remain within the responsibility of its package and
must not introduce the excluded concerns.

| Package | Responsibility | Must not contain |
| --- | --- | --- |
| `common` | Configuration, logging, and shared types | Business-specific transformations |
| `data` | Synthetic data and fixture creation | Databricks production credentials |
| `ingestion` | Source reading and Bronze writes | UI code or prompts |
| `transformation` | Silver and Gold business logic | LLM code |
| `rag` | Parsing, chunking, and retrieval | Gold metric calculations |
| `agents` | Routing and graph orchestration | Large ETL jobs |
| `api` | HTTP request and response boundary | Raw warehouse credentials |

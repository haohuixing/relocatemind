# Legacy Prompt Notice

The root `PROMPT.txt` predates the layered agent-context system. It is retained as historical material because it may contain pre-existing working-tree edits and should not be overwritten casually.

It is **not canonical**. Future agents must use:

- `AGENTS.md`;
- `PROMPT.md`;
- `docs/agent-context/PROJECT_BRIEF.md`;
- `docs/agent-context/CURRENT_STATE.md`;
- `docs/agent-context/ARCHITECTURE.md`;
- `docs/agent-context/ROADMAP.md`;
- the relevant safety, governance, provider, and operations documents.

If the historical prompt conflicts with verified code or the canonical context documents, treat the historical prompt as superseded. Archive or remove it only in a separate, explicitly scoped cleanup task after reviewing its working-tree ownership.


Stage 5: First MCP Prototype (Planner + Executor via FastAPI)
- Built two agent services (Planner + Executor) as standalone FastAPI apps
- Each exposes clean API endpoints: /plan and /execute
- Implemented orchestrator that chains both agents over HTTP
- Executor powered by real OpenAI LLM completions
- Services communicate using structured JSON via Pydantic models
- Agents run independently on different ports (MCP best practice)
- Debugged, tested, and logged the first full multi-agent interaction


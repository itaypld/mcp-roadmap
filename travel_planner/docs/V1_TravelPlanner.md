

# ✈️ V1: Travel Planner – Multi-Agent MCP System

## 🎯 Objective

This version of the Travel Planner demonstrates a functional multi-agent system based on the Model Context Protocol (MCP). It allows a user to input a natural language travel goal and receive a step-by-step itinerary using LLM-driven planning and execution agents.

---

## 🧠 Architecture

### Agents

- **Planner Agent**  
  - Input: A user travel goal (e.g., "5-day cultural trip to Japan")  
  - Output: A list of subtasks to be executed  
  - Backend: FastAPI with OpenAI GPT-3.5 for dynamic planning

- **Executor Agent**  
  - Input: A single planning step  
  - Output: A detailed, LLM-generated response  
  - Backend: FastAPI with OpenAI GPT-3.5

### Orchestrator

- Python script that:
  - Accepts a user goal
  - Sends it to the planner
  - Iterates through the planner’s steps
  - Sends each to the executor
  - Aggregates and prints/logs results

---

## 🔗 Interfaces

All communication is JSON-based over HTTP using shared Pydantic schemas.

- `POST /plan` → Planner
- `POST /execute` → Executor
- `GET /status` → Health check for each agent

---

## 🛠 Setup

### Requirements

- Python 3.9+
- `.env` file with `OPENAI_API_KEY=...`

### Run

```bash
# From the travel_planner directory:

# 1. Start planner agent
uvicorn planner_agent.main:app --reload --port 8000

# 2. Start executor agent
uvicorn executor_agent.main:app --reload --port 8001

# 3. Run orchestrator
python orchestrator/controller.py
```

---

## 📦 Features

- Modular agent services (run independently)
- Shared schema definitions (`shared_schema.py`)
- Logging to both file and console
- Error-handling and structured output
- Fully working ReAct-style planning-execution loop

---

## 📁 Folder Structure

```
travel_planner/
├── planner_agent/
├── executor_agent/
├── orchestrator/
├── shared_schema.py
└── docs/
    └── V1_TravelPlanner.md
```

---

## 🔮 Next Goals

- Add validator agent to check output consistency
- Introduce tool routing for real-time APIs (e.g., flight data)
- Add persistent memory or caching layer
- Build minimal front-end or notebook demo
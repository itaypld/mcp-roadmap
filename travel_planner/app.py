
from fastapi import FastAPI
from planner_agent.router     import router as planner_router
from executor_agent.main    import router as executor_router
from summarizer_agent.router import router as summarizer_router
from validator_agent.router   import router as validator_router

app = FastAPI(title="Travel Planner MCP")

app.include_router(planner_router,    prefix="/plan",      tags=["planner"])
app.include_router(executor_router,   prefix="/execute",   tags=["executor"])
app.include_router(summarizer_router, prefix="/summarize", tags=["summarizer"])
app.include_router(validator_router,  prefix="/validate",  tags=["validator"])




from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class PlanningRequest(BaseModel):
    goal: str

class PlanningResponse(BaseModel):
    steps: List[str]

@app.post("/plan", response_model=PlanningResponse)
async def generate_plan(request: PlanningRequest):
    # Dummy planning logic – this will be replaced by LLM logic
    steps = [
        f"Research flights and visas for: {request.goal}",
        f"Book accommodation in key areas of {request.goal}",
        f"Plan a 5-day itinerary with local cultural and nature highlights in {request.goal}"
    ]
    return PlanningResponse(steps=steps)

@app.get("/status")
def status():
    return {"status": "ok", "agent": "planner"}
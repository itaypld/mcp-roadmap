from pydantic import BaseModel
from typing import List, Optional, Any

class PlanningRequest(BaseModel):
    goal: str
    memory_summary: Optional[str] = None

class PlanningStep(BaseModel):
    tool: str
    input: Any

class PlanningResponse(BaseModel):
    steps: List[PlanningStep]

class ExecutionRequest(BaseModel):
    task: str

class ExecutionResponse(BaseModel):
    result: str
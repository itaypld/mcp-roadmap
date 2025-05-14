

from pydantic import BaseModel
from typing import List

class PlanningRequest(BaseModel):
    goal: str

class PlanningResponse(BaseModel):
    steps: List[str]

class ExecutionRequest(BaseModel):
    task: str

class ExecutionResponse(BaseModel):
    result: str
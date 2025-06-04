

import openai
import os
from fastapi import FastAPI, Request
import uvicorn

from openai import OpenAI

client = OpenAI()

def refine_plan(plan_steps, tool_outputs, summary, goal):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a travel plan refiner..."},
            {"role": "user", "content": f"Steps: {plan_steps}\nTool Outputs: {tool_outputs}\nSummary: {summary}\nGoal: {goal}"}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("travel_planner.refiner:app", host="0.0.0.0", port=8004, reload=True)


# FastAPI web server
app = FastAPI()

@app.post("/refine")
async def refine_endpoint(request: Request):
    body = await request.json()
    plan_steps = body.get("plan_steps", "")
    tool_outputs = body.get("tool_outputs", "")
    summary = body.get("summary", "")
    goal = body.get("goal", "")
    refined = refine_plan(plan_steps, tool_outputs, summary, goal)
    return {"refined_plan": refined}

if __name__ == "__main__":
    uvicorn.run("refiner:app", host="0.0.0.0", port=8004, reload=True)
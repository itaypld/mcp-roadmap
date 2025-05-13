from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

class ExecutionRequest(BaseModel):
    task: str

class ExecutionResponse(BaseModel):
    result: str

@app.post("/execute", response_model=ExecutionResponse)
async def execute_task(request: ExecutionRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Please complete this task: {request.task}"
            }]
        )
        result = response.choices[0].message.content
        return ExecutionResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

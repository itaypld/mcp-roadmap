from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
from shared_schema import ExecutionRequest, ExecutionResponse
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("executor.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()


@app.post("/execute", response_model=ExecutionResponse)
async def execute_task(request: ExecutionRequest):
    logging.info(f"[executor] Received task: {request.task}")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Please complete this task: {request.task}"
            }]
        )
        result = response.choices[0].message.content.strip()
        logging.info(f"[executor] Generated result: {result}")
        return ExecutionResponse(result=result)
    except Exception as e:
        logging.error(f"[executor] Error during execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def status():
    return {"status": "ok", "agent": "executor"}

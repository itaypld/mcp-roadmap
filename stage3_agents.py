import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def calculator_tool(expression: str) -> str:
    """Evaluates simple math expressions like '2 + 2' or '5 * (3 + 2)'."""
    try:
        result = eval(expression, {"__builtins__": {}})#restricting built-ins for security
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"
    
def plan_tasks(goal: str) -> list:
    """Planner agent: breaks down a high-level goal into subtasks."""
    messages = [
        {"role": "system", "content": "You are a project planner. Return only a numbered list of 3 clear, concise research subtasks. Do not include any headings, preamble, or extra commentary. Each subtask should be a complete sentence and directly actionable."},
        {"role": "user", "content": f"My goal: {goal}"}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    text = response.choices[0].message.content.strip()
    print("\n📋 Planned Tasks:\n", text)
    return text.split("\n")

def execute_task(task: str) -> str:
    """Executor agent: completes one task at a time using the LLM."""
    messages = [
        {"role": "system", "content": "You are a helpful research assistant."},
        {"role": "user", "content": f"Please complete the following task: {task}"}
    ]
    if "calculate" in task.lower() or "what is" in task.lower():
        # Try to extract a math expression from the task
        match = re.search(r'[\d\s\+\-\*/\(\)\.]+', task)
        if match:
            expr = match.group()
            return calculator_tool(expr)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content.strip()
def task_summarizer(tasks:list) -> str:
    """Summarizer agent: summarizes the results of the tasks."""
    messages = [
        {"role": "system", "content": "You are a summarizer. Your job is to read a series of research task results and synthesize a clear, high-level summary of the main insights. Be concise and structured."},
        {"role": "user", "content": f"Here are the task results:\n\n" + "\n\n".join(tasks)}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content.strip()
def validate_task(task: str,goal: str) -> str:
    """validateor agent: checks the summary for accuracy and completeness."""
    messages = [
        {"role": "system", "content": "You are a validator. Your job is to check the summary of the research task results for accuracy and completeness."},
        {"role": "user", "content": f"""You are given a summary generated from a series of task results. Please verify that this summary:
- Aligns with the original research goal
- Covers the key points without being too verbose
- Does not introduce unrelated content

Original goal:
{goal}

Summary:
{task}
"""}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content.strip()
if __name__ == "__main__":
    user_goal = input("Enter your goal: ")
    tasks = plan_tasks(user_goal)
    executer_log = []
    print("\n🔍 Executing Tasks:\n")
    for i, task in enumerate(tasks, start=1):
        if not task.strip() or len(task.split()) < 4:
            continue
        print(f"Task {i}: {task}")
        result = execute_task(task)
        executer_log.append(result)
        print(f"Result:\n{result}\n{'-'*60}\n")
    print("\n📜 Summary of Results:\n")
    summary = task_summarizer(executer_log)
    print(summary)
    print("\n🔍 Validating Summary:\n")
    validation = validate_task(summary,user_goal)
    print(validation)

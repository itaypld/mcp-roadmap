import requests

PLANNER_URL = "http://127.0.0.1:8000/plan"
EXECUTOR_URL = "http://127.0.0.1:8001/execute"

def orchestrate(goal: str):
    print(f"🎯 Travel Goal: {goal}\n")

    # Step 1: Get steps from the planner
    planner_response = requests.post(PLANNER_URL, json={"goal": goal})
    planner_response.raise_for_status()
    steps = planner_response.json()["steps"]

    print("🧠 Planner returned:")
    for i, step in enumerate(steps, 1):
        print(f"  Step {i}: {step}")
    print()

    # Step 2: Execute each step
    print("⚙️ Executor results:")
    for i, step in enumerate(steps, 1):
        exec_response = requests.post(EXECUTOR_URL, json={"task": step})
        exec_response.raise_for_status()
        result = exec_response.json()["result"]
        print(f"  Result {i}: {result}")

if __name__ == "__main__":
    travel_goal = "5-day cultural trip to Japan"
    orchestrate(travel_goal)

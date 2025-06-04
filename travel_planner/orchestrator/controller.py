import requests
import json
from travel_planner.memory_agent import load_memory, save_memory
from travel_planner.tools.tool_config import TOOL_URLS

PLANNER_URL     = "http://127.0.0.1:8000/plan"
AGGREGATOR_URL  = "http://127.0.0.1:8003/aggregate"

def orchestrate(goal: str):
    prev_mem = load_memory()
    if prev_mem and prev_mem.get("summary"):
        print("💾 Loaded previous summary:")
        print(prev_mem["summary"])
        print()
    print(f"🎯 Travel Goal: {goal}\n")

    # 1) Get plan from the planner
    payload = {"goal": goal}
    if prev_mem and prev_mem.get("summary"):
        payload["memory_summary"] = prev_mem["summary"]
    planner_resp = requests.post(PLANNER_URL, json=payload)
    planner_resp.raise_for_status()
    planner_data = planner_resp.json()
    print(f"🧠 Raw planner response: {planner_data}")
    steps = planner_data.get("steps", [])

    print("🧠 Planner returned:")
    for idx, step in enumerate(steps, 1):
        print(f"  Step {idx}: {step}")
    print()

    # 1.5) Refine steps using the refiner agent
    REFINER_URL = "http://127.0.0.1:8004/refine"
    refine_payload = {
        "goal": goal,
        "steps": steps,
        "memory_summary": payload.get("memory_summary", "")
    }
    refiner_resp = requests.post(REFINER_URL, json=refine_payload)
    refiner_resp.raise_for_status()
    refined_data = refiner_resp.json()
    refined_steps = refined_data.get("refined_steps", steps)
    print("🔧 Refiner returned:")
    for idx, step in enumerate(refined_steps, 1):
        print(f"  Refined Step {idx}: {step}")
    print()
    steps = refined_steps

    results = []

    # 2) Execute each step by calling the appropriate tool (or executor)
    for idx, step in enumerate(steps, 1):
        tool_name  = step["tool"]
        tool_input = step["input"]
        if tool_name not in TOOL_URLS:
            print(f"⚠️  Skipping unsupported tool: {tool_name}")
            continue

        url = TOOL_URLS[tool_name]
        if tool_name == "executor":
            payload = {"task": tool_input}
        else:
            payload = tool_input

        exec_resp = requests.post(url, json=payload)
        exec_resp.raise_for_status()
        if tool_name == "executor":
            result_str = exec_resp.json().get("result", "")
        else:
            result_str = json.dumps(exec_resp.json())

        results.append((tool_name, result_str))
        print(f"⚙️  Step {idx} ({tool_name}) Result: {result_str}")

    # 3) Aggregate results into a final report using the aggregator agent
    agg_resp = requests.post(AGGREGATOR_URL, json={"results":[{"task": t, "result": r} for t, r in results]})
    agg_resp.raise_for_status()
    new_summary = agg_resp.json()["summary"]
    save_memory(goal, results, new_summary)
    print("\n🧩 Coherent Plan Summary:")
    print(new_summary)

if __name__ == "__main__":
    travel_goal = "5-day cultural trip to Japan"
    orchestrate(travel_goal)
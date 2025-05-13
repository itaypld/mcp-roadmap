

import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculator_tool(expression: str) -> str:
    """Evaluates simple math expressions."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__": #checks if we are running this script directly
    # 1. Get user query
    query = input("Enter your question: ")

    # 2. Initialize the conversation with system and user messages
    messages = [
        {"role": "system", "content": "You are an intelligent assistant that can reason step-by-step and use tools to answer questions. You can use the tool 'Calculator' if needed. Format your reasoning like this:\nThought: ...\nAction: Calculator\nAction Input: 2 + 2\nObservation: ...\nThought: ...\nFinal Answer: ..."},
        {"role": "user", "content": query}
    ]

    while True:
        # 3. Ask the LLM what to do next
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content.strip()
        print("\n Agent Response:\n", reply)

        messages.append({"role": "assistant", "content": reply})

        # 4. Look for action
        action_match = re.search(r"Action:\s*Calculator", reply)
        input_match = re.search(r"Action Input:\s*(.+)", reply)

        if action_match and input_match:
            expression = input_match.group(1).strip()
            print(f"\n🔧 Tool Called: Calculator('{expression}')")
            result = calculator_tool(expression)
            print(f"Observation: {result}")

            # 5. Add observation to messages for next LLM step
            messages.append({"role": "user", "content": f"Observation: {result}"})
        elif "Final Answer:" in reply:
            break
        else:
            print("\n⚠️ No valid action or final answer detected. Ending loop.")
            break
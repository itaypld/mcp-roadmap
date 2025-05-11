import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create a client object
client = OpenAI(api_key=api_key)

# Open output file
output_file = open("stage1_output.md", "w", encoding="utf-8")

# Define the prompt messages
messages = [
    {"role": "user", "content": "List 3 interesting facts about honey bees."}
]

#Read and split prompt blocks from stage1_prompts.md
with open("stage1_prompts.md", "r") as f:
    content = f.read()
blocks = content.split("## Prompt")

for i, block in enumerate(blocks[1:], start=1):
    # Parse roles
    system_msg = None
    user_msg = None

    for line in block.strip().splitlines():
        if line.startswith("System:"):
            system_msg = line.replace("System:", "").strip()
        elif line.startswith("User:"):
            user_msg = line.replace("User:", "").strip()

    # Build the messages list
    messages = []
    if system_msg:
        messages.append({"role": "system", "content": system_msg})
    if user_msg:
        messages.append({"role": "user", "content": user_msg})

    # Print to confirm
    print(f"Prompt {i} messages:")
    for m in messages:
        print(f"  {m['role']}: {m['content']}")
    print()

    # Send to OpenAI and print response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    print("Response:")
    print(response.choices[0].message.content)
    print("\n🔢 Tokens used:", response.usage)
    print("="*60)

    # Write to output markdown log
    output_file.write(f"## Prompt {i}\n")
    if system_msg:
        output_file.write(f"**System:** {system_msg}\n\n")
    if user_msg:
        output_file.write(f"**User:** {user_msg}\n\n")
    output_file.write("**Response:**\n")
    output_file.write(response.choices[0].message.content.strip() + "\n\n")
    output_file.write("---\n\n")


# Close output file
output_file.close() 
from groq import Groq
import tools
import os
from dotenv import load_dotenv
client = Groq()

systemPromptFile = open("System Prompt.md", "r")
systemPrompt = systemPromptFile.read()
userPrompt = input("Enter prompt: ")
messages = [{"role": "system", "content": systemPrompt}, {"role": "user","content": userPrompt}]

iterations = 0
while True:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools.TOOL_SCHEMAS
    )
    messages.append(response.choices[0].message)
    iterations+=1
    if response.choices[0].finish_reason == "stop":
        break
    if iterations >= 100:
        break
    print(response.choices[0].message.reasoning)
    for tool_call in response.choices[0].message.tool_calls:
        function_response = tools.execute_tool_call(tool_call)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": str(function_response)
        })

print("finished")
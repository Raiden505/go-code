from groq import Groq
import tools
import os
from dotenv import load_dotenv
client = Groq()

messages = [{"role": "user","content": "make a new file called hello.txt and write the word 'hello' in it"}]

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=tools.TOOL_SCHEMAS
)

messages.append(response.choices[0].message)

if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        function_response = tools.execute_tool_call(tool_call)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": str(function_response)
        })
    final = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )
    
    print(final.choices[0].message)
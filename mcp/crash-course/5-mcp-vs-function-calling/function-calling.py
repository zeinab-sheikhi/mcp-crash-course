import json

import openai
from dotenv import load_dotenv

from tools import add


load_dotenv()

"""This is a simple example to demonstrate that MCP simply enables a new way to call functions."""


tools = [
    {
        "type": "function", 
        "function": {
            "name": "add", 
            "description": "Add two integers numbers together",
            "parameters": {
                "type": "object", 
                "properties": {
                    "a": {"type": "integer", "description": "First number"},
                    "b": {"type": "integer", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    },
]

# LLm call
response = openai.chat.completions.create(
    model="gpt-4o", 
    messages=[{"role": "user", "content": "Calculate 25 + 17"}],
    tools=tools, 
    tool_choice="auto",
)

# handle tool call
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)

    result = add(**tool_args)

    # send the result back to the model
    final_response = openai.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "user", "content": "Calculate 25 + 17"},
            response.choices[0].message,
            {"role": "tool", "tool_call_id": tool_call.id, "content": str(result)}
        ],
    )

    print(final_response.choices[0].message.content)

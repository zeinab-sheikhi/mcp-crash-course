import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from dotevn import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client import stdio_client
from openai import AsyncOpenAI

load_dotenv()

class MCPOpenAIClient:
    """Client for interacting with MCP models using MCP tools."""
    def __init__(self, model: str = "gpt-4o"):
        """Initialize the OpenAI MCP client.
        Args:
            model (str): The OpenAI model to use.
        """
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI()
        self.model = model
        self.stdio = Optional[Any] = None
        self.write = Optional[Any] = None
    
    async def connect_to_server(self, server_script_path: str = "server.py"):
        """onnect to MCP server
        Args:
            server_script_path: The path to the MCP server script.
        """
        server_params = StdioServerParameters(
            command="python", 
            args=[server_script_path],
        )
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()
        
        # list available tools
        tools_result = await self.session.list_tools()
        print("Connected to server with tools")
        for tool in tools_result.tools:
            print(f" - {tool.name}: {tool.description}")
        

        
    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """Get available tools from MCP server in OpenAI format.
        
        Returns:
            List[Dict[str, Any]]: A list of tools in OpenAI format.
        """
        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function", 
                "function": {
                    "name": tool.name, 
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
                
            } 
            for tool in tools_result.tools
        ]
    
    async def process_query(self, query: str) -> str:
        """Process a query using OpenAI and available MCP tools.

        Args:
            query (str): The query to process.

        Returns:
            str: The response from the OpenAI API.
        """
        
        tools = await self.get_mcp_tools()
        response = await self.openai_client.chat.completions.create(
            model=self.model, 
            messages=[{"role": "user", "content": query}],
            tools=tools, 
            tool_choice="auto",
        )

        # Get assistant response
        assistant_message = response.choices[0].message

        # Initialize conversation with user query and assistant response
        messages = [
            {"role": 'user', "content": query},
            assistant_message,
        ]
        
        # Handle tool calls if present
        if assistant_message.tool_calls:
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                # Execute tool call
                result = await self.session.call_tool(
                    tool_call.function.name, 
                    arguments=json.load(tool_call.function.arguments),
                )

                # add tool response to the conversation
                messages.append(
                    {
                        "role": "tool", 
                        "tool_call_id": tool_call.id, 
                        "content": result.content[0].text,
                    }
                )
            
            # Get final response from OpenAI with tool results
            final_response = await self.openai_client.chat.completions.create(
                model=self.model, 
                messages=messages, 
                tools=tools, 
                tool_choice="none",
            )

            return final_response.choices[0].message.content
        
        # no tool call, just return the direct response
        return assistant_message.content

    async def clean_up(self):
        """Clean up resources."""
        await self.exit_stack.aclose()


async def main():
    """Main entry point for the client."""
    client = MCPOpenAIClient()
    await client.connect_to_server("server.py")

    query = "What is our company vaacation policy?"
    print(f"Query: {query}")

    response = await client.process_query(query)
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())

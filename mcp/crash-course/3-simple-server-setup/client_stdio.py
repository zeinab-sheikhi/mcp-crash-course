import asyncio
# import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# nest_asyncio.apply()  # needed to run interactive python

async def main():
    server_params = StdioServerParameters(
        command="python", 
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # list available tools
            tools_result = await session.list_tools()
            print("Available tools: ")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # call our calculator tool
            result = await session.call("add", arguments={"a": 1, "b": 2})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())


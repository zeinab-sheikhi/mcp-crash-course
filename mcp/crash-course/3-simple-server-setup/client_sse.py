import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

"""
Make sure:
- the server is running before satrting the client.
- The server is configured to use SSE transport.
- The server is listening on port 8050.
"""

async def main():
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = session.list_tools()
            print("Available tools: ")
            for tool in tools_result:
                print(f"- {tool.name}: {tool.description}")

            # call our calculator tool
            result = await session.call("add", arguments={"a": 1, "b": 2})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
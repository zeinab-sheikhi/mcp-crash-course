import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    # connect to the server using SSE transport
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # list all the available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            # call our calculator tool
            result = await session.call_tool("calculator", arguments={"a": 25, "b": 17})
            print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())

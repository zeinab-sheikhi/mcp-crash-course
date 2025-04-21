from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(
    name="Calculator", 
    host="0.0.0.0", 
    port=8050,
)

@mcp.tool()
def calculator(a: int, b: int) -> int:
    """Add two integer numbers together"""
    return a + b

if __name__ == "__main__":
    print("Running MCP with SSE transport.")
    mcp.run(transport="sse")

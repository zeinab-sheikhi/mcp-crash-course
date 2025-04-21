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

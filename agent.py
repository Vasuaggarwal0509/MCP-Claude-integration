# ANSI color codes for better log visibility
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RESET = "\033[0m"
SEP = "=" * 40

"""
This file is just a demo with addition fuctionality.
It shows how to set up an MCP client that connects to an MCP server.

"""



import os
import json
from typing import List, Dict, Any

# MCP client libraries
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Gemini (free tier)
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()   # loads GOOGLE_API_KEY from .env

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.0
)

print("Gemini + MCP Client Setup Complete!")



async def discover_tools():
    """
    Connect to the MCP server and discover available tools.
    Returns a list of available tools with their schemas.
    """

    # Run your MCP server through Python + script path
    server_params = StdioServerParameters(
        command="python",
        args=[mcp_server_path],   # your MCP server script path
    )

    print(f"{BLUE}{SEP}\n🔍 Connecting to MCP server...{RESET}")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print(f"{BLUE}📡 Initializing MCP connection...{RESET}")
            await session.initialize()

            print(f"{BLUE}🔎 Listing tools...{RESET}")
            tools = await session.list_tools()

            tool_info = []
            for tool_type, tool_list in tools:
                if tool_type == "tools":
                    for tool in tool_list:
                        tool_info.append({
                            "name": tool.name,
                            "description": tool.description,
                            "schema": tool.inputSchema
                        })

            print(f"{GREEN}✅ Found {len(tool_info)} tools{RESET}")
            print(SEP)

            return tool_info





async def ask_gemini_and_call_tools(prompt: str):
    """
    Gemini decides which MCP tool to call.
    Then this function calls the tool via MCP client.
    """

    # Ask Gemini what tool to use
    reasoning = llm.invoke(
        f"""
        You have access to external MCP tools.
        Here is the user prompt:

        {prompt}

        Based on the user request,
        return ONLY a JSON:
        {{
          "tool": "<tool_name>",
          "arguments": {{"a": 5, "b": 10}}  # example
        }}

        If no tool is needed, return:
        {{
            "tool": null,
            "arguments": null
        }}
        """
    )

    print("\n🧠 Gemini Decision:")
    print(reasoning)

    try:
        decision = json.loads(reasoning)
    except:
        return "Gemini returned invalid JSON."

    tool_name = decision["tool"]
    tool_args = decision["arguments"]

    if tool_name is None:
        return "Gemini thinks no tool is needed."

    print(f"\n🔧 Gemini selected tool: {tool_name}")
    print(f"🔢 Args: {tool_args}")

    # Now use MCP to run the selected tool
    server_params = StdioServerParameters(command="python", args=[mcp_server_path])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                name=tool_name,
                arguments=tool_args
            )

            print("\n🟩 Tool result:")
            print(result)
            return result





import asyncio

mcp_server_path = "D:\\MCP server learning\\mcp_tools.py"

tools = asyncio.run(discover_tools())
print(tools)

response = asyncio.run(ask_gemini_and_call_tools("Add 12 and 17"))
print(response)

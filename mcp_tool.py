# mcp_tools.py
# Simplest MCP server with one tool: add(a, b)
# IMPORTANT: only log to stderr, stdout must be clean for JSON-RPC.

import sys

try:
    from mcp.server.fastmcp import FastMCP   # for mcp[cli]
except:
    from mcp import FastMCP   # fallback for mcp-server package

# Create simple MCP server
mcp = FastMCP("simple_math")


# --------------- TOOL: add two numbers ------------------
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    
    return a * b


# -------------------- RUN SERVER ------------------------
def main():
    print("[stderr] Starting Simple MCP Math Server...", file=sys.stderr)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

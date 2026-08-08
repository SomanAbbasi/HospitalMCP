from mcp.server.fastmcp import FastMCP

from doctors import search_doctors


mcp = FastMCP("Hospital MCP Server")


@mcp.tool()
def search_hospital_doctors(specialty: str) -> list[dict]:
    """Search hospital doctors by medical specialty."""
    return search_doctors(specialty)


if __name__ == "__main__":
    mcp.run()
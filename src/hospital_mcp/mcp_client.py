import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_path = Path(__file__).with_name("mcp_server.py")

    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", str(server_path)],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool(
                "search_hospital_doctors",
                arguments={"specialty": "Cardiology"},
            )

            print("\nSearch result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())

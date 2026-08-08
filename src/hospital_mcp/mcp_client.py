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

            print("\nAvailable tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")
                print(f"  Description: {tool.description}")
                print(f"  Input schema: {tool.inputSchema}")

            doctor_search = await session.call_tool(
                "search_hospital_doctors",
                arguments={"specialty": "Cardiology"},
            )

            print("\nCardiology search:")
            print(doctor_search)

            doctor = await session.call_tool(
                "get_hospital_doctor",
                arguments={"doctor_id": "D001"},
            )

            print("\nDoctor D001:")
            print(doctor)

            availability = await session.call_tool(
                "get_hospital_doctor_availability",
                arguments={"doctor_id": "D001"},
            )

            print("\nAvailability:")
            print(availability)


if __name__ == "__main__":
    asyncio.run(main())

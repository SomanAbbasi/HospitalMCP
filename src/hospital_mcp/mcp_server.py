from mcp.server.fastmcp import FastMCP

from doctors import search_doctors,get_doctor,get_doctor_availability


mcp = FastMCP("Hospital MCP Server")


@mcp.tool()
def search_hospital_doctors(specialty: str) -> list[dict]:
    """Search hospital doctors by medical specialty."""
    return search_doctors(specialty)

@mcp.tool()
def get_hospital_doctor(doctor_id: str) -> dict:
    """Get a hospital doctor by their unique doctor ID."""

    doctor = get_doctor(doctor_id)

    if doctor is None:
        raise ValueError(f"Doctor '{doctor_id}' was not found.")

    return doctor

@mcp.tool()
def get_hospital_doctor_availability(doctor_id: str) -> list[str]:
    """Get available appointment time slots for a hospital doctor."""
    return get_doctor_availability(doctor_id)

if __name__ == "__main__":
    mcp.run()
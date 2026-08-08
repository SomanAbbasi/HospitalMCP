from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

from doctors import search_doctors, get_doctor, get_doctor_availability

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


@mcp.resource("hospital://specialties")
def hospital_specialties() -> str:
    """List the medical specialties available at the hospital."""

    return """
        Cardiology
        Neurology
        Dermatology
        """


@mcp.resource("hospital://info")
def hospital_info() -> str:
    """Basic information about the hospital."""

    return """
        Hospital: City Care Hospital

        Departments:
        - Cardiology
        - Neurology
        - Dermatology

        Emergency Department:
        24/7
        """


@mcp.prompt()
def doctor_consultation(question: str, specialty: str) -> list[base.Message]:
    """Prepare a structured prompt for a hospital doctor consultation."""

    return [
        base.UserMessage(
            content=base.TextContent(
                type="text",
                text=(
                    f"I need help with a hospital consultation.\n\n"
                    f"Patient question: {question}\n"
                    f"Relevant specialty: {specialty}\n\n"
                    "Analyze the request carefully and identify what "
                    "information should be gathered next."
                ),
            )
        )
    ]


if __name__ == "__main__":
    mcp.run()

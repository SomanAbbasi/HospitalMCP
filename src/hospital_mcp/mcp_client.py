import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def extract_tool_result(tool_result: object) -> object:
    structured_content = getattr(tool_result, "structured_content", None)
    if isinstance(structured_content, dict) and "result" in structured_content:
        return structured_content["result"]

    content = getattr(tool_result, "content", None)
    if content:
        first_item = content[0]
        text = getattr(first_item, "text", None)
        if isinstance(text, str):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text

    return None


async def main() -> None:
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "hospital_mcp.mcp_server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("\nAvailable tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")
                print(f"  Description: {tool.description}")
                print(f"  Input schema: {tool.input_schema}")

            resources = await session.list_resources()

            print("\nAvailable resources:")

            for resource in resources.resources:
                print(f"- {resource.uri}")
                print(f"  Name: {resource.name}")

            prompts = await session.list_prompts()

            print("\nAvailable prompts:")

            for prompt in prompts.prompts:
                print(f"- {prompt.name}")
                print(f"  Description: {prompt.description}")

            prompt = await session.get_prompt(
                "doctor_consultation",
                arguments={
                    "question": "Patient has recurring chest pain.",
                    "specialty": "Cardiology",
                },
            )

            print("\nDoctor consultation prompt:")

            for message in prompt.messages:
                print(message)

            specialties = await session.read_resource("hospital://specialties")

            print("\nHospital specialties:")
            print(specialties)

            overview = await session.read_resource("hospital://overview")

            print("\nHospital overview:")
            print(overview)

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

            patient = await session.call_tool(
                "get_hospital_patient",
                arguments={"patient_id": "P001"},
            )

            print("\nPatient P001:")
            print(patient)

            patient_records = await session.call_tool(
                "get_hospital_patient_records",
                arguments={"patient_id": "P001"},
            )

            print("\nPatient P001 records:")
            print(patient_records)

            patient_appointments = await session.call_tool(
                "get_hospital_patient_appointments",
                arguments={"patient_id": "P001"},
            )

            print("\nPatient P001 appointments:")
            print(patient_appointments)

            available_slots = await session.call_tool(
                "search_hospital_available_slots",
                arguments={"doctor_id": "D001"},
            )

            print("\nAvailable slots for D001:")
            print(available_slots)

            booking = await session.call_tool(
                "book_hospital_appointment",
                arguments={
                    "patient_id": "P001",
                    "doctor_id": "D001",
                    "scheduled_at": "2026-08-10 09:00",
                },
            )

            print("\nBooked appointment:")
            print(booking)

            booking_result = extract_tool_result(booking)
            if not isinstance(booking_result, dict):
                raise RuntimeError("Booking tool did not return structured appointment data.")

            invoice_id = booking_result["invoice"]["id"]
            appointment_id = booking_result["appointment"]["id"]

            invoice = await session.call_tool(
                "get_hospital_invoice",
                arguments={"invoice_id": invoice_id},
            )

            print("\nInvoice:")
            print(invoice)

            estimated_bill = await session.call_tool(
                "calculate_hospital_estimated_bill",
                arguments={"doctor_id": "D001"},
            )

            print("\nEstimated bill:")
            print(estimated_bill)

            patient_balance = await session.call_tool(
                "get_hospital_patient_balance",
                arguments={"patient_id": "P001"},
            )

            print("\nPatient balance:")
            print(patient_balance)

            rescheduled = await session.call_tool(
                "reschedule_hospital_appointment",
                arguments={
                    "appointment_id": appointment_id,
                    "new_scheduled_at": "2026-08-10 10:00",
                },
            )

            print("\nRescheduled appointment:")
            print(rescheduled)

            cancelled = await session.call_tool(
                "cancel_hospital_appointment",
                arguments={"appointment_id": appointment_id},
            )

            print("\nCancelled appointment:")
            print(cancelled)

            availability = await session.call_tool(
                "get_hospital_doctor_availability",
                arguments={"doctor_id": "D001"},
            )

            print("\nAvailability:")
            print(availability)


if __name__ == "__main__":
    asyncio.run(main())

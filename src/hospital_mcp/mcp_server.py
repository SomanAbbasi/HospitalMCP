from mcp.server.mcpserver import MCPServer

from hospital_mcp.appointments import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment,
    search_available_slots,
)
from hospital_mcp.billing import calculate_estimated_bill, get_invoice, get_patient_balance
from hospital_mcp.doctors import get_doctor, get_doctor_availability, search_doctors
from hospital_mcp.hospital_store import BILLING_SERVICES, DEPARTMENTS, SPECIALTIES
from hospital_mcp.patients import get_patient, get_patient_appointments, get_patient_records

mcp = MCPServer("Hospital MCP Server")


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


@mcp.tool()
def get_hospital_patient(patient_id: str) -> dict:
    """Get a patient by their unique patient ID."""

    patient = get_patient(patient_id)

    if patient is None:
        raise ValueError(f"Patient '{patient_id}' was not found.")

    return patient


@mcp.tool()
def get_hospital_patient_records(patient_id: str) -> list[dict]:
    """Get medical records for a patient."""
    return get_patient_records(patient_id)


@mcp.tool()
def get_hospital_patient_appointments(patient_id: str) -> list[dict]:
    """Get appointments for a patient."""
    return get_patient_appointments(patient_id)


@mcp.tool()
def search_hospital_available_slots(doctor_id: str) -> list[str]:
    """Search available appointment slots for a doctor."""
    return search_available_slots(doctor_id)


@mcp.tool()
def book_hospital_appointment(patient_id: str, doctor_id: str, scheduled_at: str) -> dict:
    """Book a new hospital appointment."""
    return book_appointment(patient_id, doctor_id, scheduled_at)


@mcp.tool()
def cancel_hospital_appointment(appointment_id: str) -> dict:
    """Cancel an existing hospital appointment."""
    return cancel_appointment(appointment_id)


@mcp.tool()
def reschedule_hospital_appointment(appointment_id: str, new_scheduled_at: str) -> dict:
    """Reschedule an existing hospital appointment."""
    return reschedule_appointment(appointment_id, new_scheduled_at)


@mcp.tool()
def get_hospital_invoice(invoice_id: str) -> dict:
    """Get an invoice by its unique invoice ID."""

    invoice = get_invoice(invoice_id)

    if invoice is None:
        raise ValueError(f"Invoice '{invoice_id}' was not found.")

    return invoice


@mcp.tool()
def get_hospital_patient_balance(patient_id: str) -> dict:
    """Get the current outstanding balance for a patient."""
    return get_patient_balance(patient_id)


@mcp.tool()
def calculate_hospital_estimated_bill(doctor_id: str, include_lab: bool = False) -> dict:
    """Calculate an estimated bill for a consultation."""
    return calculate_estimated_bill(doctor_id, include_lab)


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


@mcp.resource("hospital://departments")
def hospital_departments() -> list[dict[str, str]]:
    """List the hospital departments and their focus areas."""

    return DEPARTMENTS


@mcp.resource("hospital://billing/services")
def hospital_billing_services() -> list[dict[str, object]]:
    """List the billing services and baseline fees."""

    return BILLING_SERVICES


@mcp.resource("hospital://overview")
def hospital_overview() -> dict[str, object]:
    """Summarize the current hospital demo data."""

    return {
        "hospital": "City Care Hospital",
        "specialties": list(SPECIALTIES),
        "doctors": len(search_doctors("Cardiology")) + len(search_doctors("Neurology")) + len(search_doctors("Dermatology")),
        "departments": len(DEPARTMENTS),
    }


@mcp.prompt()
def doctor_consultation(question: str, specialty: str) -> list[str]:
    """Prepare a structured prompt for a hospital doctor consultation."""

    return [
        (
            f"I need help with a hospital consultation.\n\n"
            f"Patient question: {question}\n"
            f"Relevant specialty: {specialty}\n\n"
            "Analyze the request carefully and identify what "
            "information should be gathered next."
        )
    ]


@mcp.prompt()
def appointment_assistant(patient_id: str, specialty: str) -> list[str]:
    """Prepare a structured prompt for booking an appointment."""

    return [
        (
            f"I need to book a hospital appointment.\n\n"
            f"Patient ID: {patient_id}\n"
            f"Specialty: {specialty}\n\n"
            "First find a matching doctor, then check availability, "
            "then ask for confirmation of the preferred slot."
        )
    ]


if __name__ == "__main__":
    mcp.run()

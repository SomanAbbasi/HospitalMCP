from hospital_mcp.appointments import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment,
    search_available_slots,
)
from hospital_mcp.billing import calculate_estimated_bill, get_patient_balance
from hospital_mcp.doctors import get_doctor_availability, search_doctors
from hospital_mcp.patients import get_patient, get_patient_appointments, get_patient_records


def test_patient_profile_and_records() -> None:
    patient = get_patient("P001")

    assert patient is not None
    assert patient["name"] == "Adeel Rahman"

    records = get_patient_records("P001")
    appointments = get_patient_appointments("P001")

    assert len(records) == 1
    assert records[0]["summary"] == "Routine hypertension follow-up."
    assert appointments == []


def test_booking_flow_creates_invoice_and_updates_availability() -> None:
    slots = search_available_slots("D001")
    booking = book_appointment("P001", "D001", slots[0])

    assert booking["appointment"]["id"] == "A001"
    assert booking["invoice"]["id"] == "INV-001"
    assert slots[0] not in get_doctor_availability("D001")

    balance = get_patient_balance("P001")

    assert balance["patient_id"] == "P001"
    assert balance["outstanding_balance"] == 80.0


def test_reschedule_and_cancel_appointment() -> None:
    booking = book_appointment("P001", "D001", search_available_slots("D001")[0])
    appointment_id = booking["appointment"]["id"]

    rescheduled = reschedule_appointment(appointment_id, "2026-08-10 10:00")
    cancelled = cancel_appointment(appointment_id)

    assert rescheduled["appointment"]["scheduled_at"] == "2026-08-10 10:00"
    assert cancelled["appointment"]["status"] == "cancelled"


def test_estimated_bill_breakdown() -> None:
    estimate = calculate_estimated_bill("D001", include_lab=True)

    assert estimate["specialty"] == "Cardiology"
    assert estimate["total"] == 105.0


def test_search_doctors_remains_case_insensitive() -> None:
    doctors = search_doctors("CARDIOLOGY")

    assert len(doctors) == 2
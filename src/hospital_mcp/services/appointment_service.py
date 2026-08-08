from hospital_mcp.hospital_store import (
    APPOINTMENTS,
    AppointmentRecord,
    copy_appointment,
    get_appointment_record,
    get_doctor_record,
    get_patient_record,
    next_appointment_id,
    scheduled_slots_for_doctor,
)
from hospital_mcp.services.billing_service import create_invoice_for_appointment
from hospital_mcp.services.doctor_service import get_doctor_availability


def search_available_slots(doctor_id: str) -> list[str]:
    return get_doctor_availability(doctor_id)


def book_appointment(patient_id: str, doctor_id: str, scheduled_at: str) -> dict:
    patient = get_patient_record(patient_id)
    if patient is None:
        raise ValueError(f"Patient '{patient_id}' was not found.")

    doctor = get_doctor_record(doctor_id)
    if doctor is None:
        raise ValueError(f"Doctor '{doctor_id}' was not found.")

    available_slots = get_doctor_availability(doctor_id)
    if scheduled_at not in available_slots:
        raise ValueError(
            f"Doctor '{doctor_id}' is not available at '{scheduled_at}'."
        )

    appointment_id = next_appointment_id()
    appointment: AppointmentRecord = {
        "id": appointment_id,
        "patient_id": patient["id"],
        "doctor_id": doctor["id"],
        "scheduled_at": scheduled_at,
        "status": "scheduled",
    }
    APPOINTMENTS[appointment_id] = appointment

    invoice = create_invoice_for_appointment(
        appointment_id=appointment_id,
        patient_id=patient["id"],
        doctor_id=doctor["id"],
    )

    return {
        "appointment": copy_appointment(appointment),
        "invoice": invoice,
        "available_slots": get_doctor_availability(doctor_id),
    }


def cancel_appointment(appointment_id: str) -> dict:
    appointment = get_appointment_record(appointment_id)
    if appointment is None:
        raise ValueError(f"Appointment '{appointment_id}' was not found.")

    if appointment["status"] == "cancelled":
        return {
            "appointment": copy_appointment(appointment),
            "message": "Appointment was already cancelled.",
        }

    appointment["status"] = "cancelled"
    APPOINTMENTS[appointment_id] = appointment

    return {
        "appointment": copy_appointment(appointment),
        "message": "Appointment cancelled.",
    }


def reschedule_appointment(appointment_id: str, new_scheduled_at: str) -> dict:
    appointment = get_appointment_record(appointment_id)
    if appointment is None:
        raise ValueError(f"Appointment '{appointment_id}' was not found.")

    if appointment["status"] == "cancelled":
        raise ValueError("Cancelled appointments cannot be rescheduled.")

    doctor_id = appointment["doctor_id"]
    available_slots = get_doctor_availability(doctor_id)
    if new_scheduled_at not in available_slots:
        raise ValueError(
            f"Doctor '{doctor_id}' is not available at '{new_scheduled_at}'."
        )

    appointment["scheduled_at"] = new_scheduled_at
    APPOINTMENTS[appointment_id] = appointment

    return {
        "appointment": copy_appointment(appointment),
        "available_slots": get_doctor_availability(doctor_id),
    }


def get_booked_slots_for_doctor(doctor_id: str) -> set[str]:
    return scheduled_slots_for_doctor(doctor_id)
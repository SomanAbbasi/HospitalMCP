from hospital_mcp.hospital_store import (
    copy_appointment,
    copy_medical_record,
    copy_patient,
    get_medical_records,
    get_patient_record,
    scheduled_appointments_for_patient,
)


def get_patient(patient_id: str) -> dict | None:
    patient = get_patient_record(patient_id)

    if patient is None:
        return None

    return copy_patient(patient)


def get_patient_records(patient_id: str) -> list[dict]:
    return [
        copy_medical_record(record)
        for record in get_medical_records(patient_id)
    ]


def get_patient_appointments(patient_id: str) -> list[dict]:
    return [
        copy_appointment(appointment)
        for appointment in scheduled_appointments_for_patient(patient_id)
    ]
from hospital_mcp.hospital_store import (
    copy_doctor,
    get_doctor_record,
    normalize_specialty,
    scheduled_slots_for_doctor,
)


def search_doctors(specialty: str) -> list[dict]:
    normalized_specialty = normalize_specialty(specialty)

    return [
        copy_doctor(doctor)
        for doctor in get_all_doctors()
        if doctor["specialty"].lower() == normalized_specialty
    ]


def get_doctor(doctor_id: str) -> dict | None:
    doctor = get_doctor_record(doctor_id)

    if doctor is None:
        return None

    return copy_doctor(doctor)


def get_doctor_availability(doctor_id: str) -> list[str]:
    doctor = get_doctor_record(doctor_id)

    if doctor is None:
        return []

    booked_slots = scheduled_slots_for_doctor(doctor_id)

    return [
        slot
        for slot in doctor["availability"]
        if slot not in booked_slots
    ]


def get_all_doctors() -> list[dict]:
    return [copy_doctor(doctor) for doctor in _all_doctor_records()]


def _all_doctor_records() -> list[dict]:
    from hospital_mcp.hospital_store import DOCTORS

    return list(DOCTORS.values())

from typing import TypedDict


class Doctor(TypedDict):
    id: str
    name: str
    specialty: str
    experience_years: int


DOCTORS: list[Doctor] = [
    {
        "id": "D001",
        "name": "Dr. Ahmed Khan",
        "specialty": "Cardiology",
        "experience_years": 12,
    },
    {
        "id": "D002",
        "name": "Dr. Sara Ali",
        "specialty": "Neurology",
        "experience_years": 8,
    },
    {
        "id": "D003",
        "name": "Dr. Hassan Malik",
        "specialty": "Cardiology",
        "experience_years": 15,
    },
    {
        "id": "D004",
        "name": "Dr. Ayesha Noor",
        "specialty": "Dermatology",
        "experience_years": 6,
    },
]


def search_doctors(specialty: str) -> list[Doctor]:
    normalized_specialty = specialty.strip().lower()

    return [
        doctor
        for doctor in DOCTORS
        if doctor["specialty"].lower() == normalized_specialty
    ]
    
    
def get_doctor(doctor_id: str) -> Doctor | None:
    normalized_id = doctor_id.strip().upper()

    for doctor in DOCTORS:
        if doctor["id"] == normalized_id:
            return doctor

    return None
from __future__ import annotations

from copy import deepcopy
from typing import Literal, TypedDict


class DoctorRecord(TypedDict):
    id: str
    name: str
    specialty: str
    experience_years: int
    availability: list[str]


class PatientRecord(TypedDict):
    id: str
    name: str
    age: int
    primary_doctor_id: str
    conditions: list[str]


class MedicalRecord(TypedDict):
    id: str
    patient_id: str
    summary: str
    notes: list[str]
    created_at: str


class AppointmentRecord(TypedDict):
    id: str
    patient_id: str
    doctor_id: str
    scheduled_at: str
    status: Literal["scheduled", "cancelled"]


class InvoiceItem(TypedDict):
    description: str
    amount: float


class InvoiceRecord(TypedDict):
    id: str
    patient_id: str
    appointment_id: str
    items: list[InvoiceItem]
    total: float
    paid: bool


SPECIALTIES: tuple[str, ...] = (
    "Cardiology",
    "Neurology",
    "Dermatology",
)

DEPARTMENTS: list[dict[str, str]] = [
    {
        "name": "Cardiology",
        "description": "Heart and blood vessel care.",
    },
    {
        "name": "Neurology",
        "description": "Brain, nerve, and nervous system care.",
    },
    {
        "name": "Dermatology",
        "description": "Skin, hair, and nail care.",
    },
]

BILLING_SERVICES: list[dict[str, object]] = [
    {
        "name": "Consultation",
        "description": "Standard specialist consultation fee.",
        "fees": {
            "Cardiology": 80.0,
            "Neurology": 70.0,
            "Dermatology": 60.0,
        },
    },
    {
        "name": "Lab Add-On",
        "description": "Optional lab estimate added to a consultation.",
        "fee": 25.0,
    },
]

DEFAULT_DOCTORS: dict[str, DoctorRecord] = {
    "D001": {
        "id": "D001",
        "name": "Dr. Ahmed Khan",
        "specialty": "Cardiology",
        "experience_years": 12,
        "availability": [
            "2026-08-10 09:00",
            "2026-08-10 10:00",
            "2026-08-10 14:00",
        ],
    },
    "D002": {
        "id": "D002",
        "name": "Dr. Sara Ali",
        "specialty": "Neurology",
        "experience_years": 8,
        "availability": [
            "2026-08-10 11:00",
            "2026-08-10 15:00",
        ],
    },
    "D003": {
        "id": "D003",
        "name": "Dr. Hassan Malik",
        "specialty": "Cardiology",
        "experience_years": 15,
        "availability": [
            "2026-08-10 09:00",
            "2026-08-10 13:00",
        ],
    },
    "D004": {
        "id": "D004",
        "name": "Dr. Ayesha Noor",
        "specialty": "Dermatology",
        "experience_years": 6,
        "availability": [
            "2026-08-10 10:00",
            "2026-08-10 16:00",
        ],
    },
}

DEFAULT_PATIENTS: dict[str, PatientRecord] = {
    "P001": {
        "id": "P001",
        "name": "Adeel Rahman",
        "age": 34,
        "primary_doctor_id": "D001",
        "conditions": ["Hypertension"],
    },
    "P002": {
        "id": "P002",
        "name": "Mariam Shah",
        "age": 29,
        "primary_doctor_id": "D002",
        "conditions": ["Migraines"],
    },
    "P003": {
        "id": "P003",
        "name": "Fatima Noor",
        "age": 41,
        "primary_doctor_id": "D004",
        "conditions": ["Eczema"],
    },
}

DEFAULT_MEDICAL_RECORDS: dict[str, list[MedicalRecord]] = {
    "P001": [
        {
            "id": "MR001",
            "patient_id": "P001",
            "summary": "Routine hypertension follow-up.",
            "notes": [
                "Blood pressure controlled with medication.",
                "Diet and exercise guidance reviewed.",
            ],
            "created_at": "2026-08-01",
        }
    ],
    "P002": [
        {
            "id": "MR002",
            "patient_id": "P002",
            "summary": "Neurology consultation for recurring migraines.",
            "notes": [
                "Headache diary recommended.",
                "Neurology imaging reviewed.",
            ],
            "created_at": "2026-08-02",
        }
    ],
    "P003": [
        {
            "id": "MR003",
            "patient_id": "P003",
            "summary": "Dermatology review for eczema flare-up.",
            "notes": [
                "Topical treatment prescribed.",
                "Skin care routine explained.",
            ],
            "created_at": "2026-08-03",
        }
    ],
}

DOCTORS: dict[str, DoctorRecord] = {}
PATIENTS: dict[str, PatientRecord] = {}
MEDICAL_RECORDS: dict[str, list[MedicalRecord]] = {}
APPOINTMENTS: dict[str, AppointmentRecord] = {}
INVOICES: dict[str, InvoiceRecord] = {}
APPOINTMENT_SEQUENCE = 1
INVOICE_SEQUENCE = 1


def reset_demo_state() -> None:
    global DOCTORS, PATIENTS, MEDICAL_RECORDS, APPOINTMENTS, INVOICES
    global APPOINTMENT_SEQUENCE, INVOICE_SEQUENCE

    DOCTORS.clear()
    DOCTORS.update(deepcopy(DEFAULT_DOCTORS))

    PATIENTS.clear()
    PATIENTS.update(deepcopy(DEFAULT_PATIENTS))

    MEDICAL_RECORDS.clear()
    MEDICAL_RECORDS.update(deepcopy(DEFAULT_MEDICAL_RECORDS))

    APPOINTMENTS.clear()
    INVOICES.clear()
    APPOINTMENT_SEQUENCE = 1
    INVOICE_SEQUENCE = 1


def normalize_identifier(value: str) -> str:
    return value.strip().upper()


def normalize_specialty(value: str) -> str:
    return value.strip().lower()


def next_appointment_id() -> str:
    global APPOINTMENT_SEQUENCE

    appointment_id = f"A{APPOINTMENT_SEQUENCE:03d}"
    APPOINTMENT_SEQUENCE += 1
    return appointment_id


def next_invoice_id() -> str:
    global INVOICE_SEQUENCE

    invoice_id = f"INV-{INVOICE_SEQUENCE:03d}"
    INVOICE_SEQUENCE += 1
    return invoice_id


def copy_doctor(record: DoctorRecord) -> DoctorRecord:
    return deepcopy(record)


def copy_patient(record: PatientRecord) -> PatientRecord:
    return deepcopy(record)


def copy_medical_record(record: MedicalRecord) -> MedicalRecord:
    return deepcopy(record)


def copy_appointment(record: AppointmentRecord) -> AppointmentRecord:
    return deepcopy(record)


def copy_invoice(record: InvoiceRecord) -> InvoiceRecord:
    return deepcopy(record)


def get_doctor_record(doctor_id: str) -> DoctorRecord | None:
    return DOCTORS.get(normalize_identifier(doctor_id))


def get_patient_record(patient_id: str) -> PatientRecord | None:
    return PATIENTS.get(normalize_identifier(patient_id))


def get_medical_records(patient_id: str) -> list[MedicalRecord]:
    return MEDICAL_RECORDS.get(normalize_identifier(patient_id), [])


def get_appointment_record(appointment_id: str) -> AppointmentRecord | None:
    return APPOINTMENTS.get(normalize_identifier(appointment_id))


def get_invoice_record(invoice_id: str) -> InvoiceRecord | None:
    return INVOICES.get(normalize_identifier(invoice_id))


def scheduled_slots_for_doctor(doctor_id: str) -> set[str]:
    normalized_id = normalize_identifier(doctor_id)

    return {
        appointment["scheduled_at"]
        for appointment in APPOINTMENTS.values()
        if appointment["doctor_id"] == normalized_id and appointment["status"] == "scheduled"
    }


def scheduled_appointments_for_patient(patient_id: str) -> list[AppointmentRecord]:
    normalized_id = normalize_identifier(patient_id)

    return [
        copy_appointment(appointment)
        for appointment in APPOINTMENTS.values()
        if appointment["patient_id"] == normalized_id
    ]


reset_demo_state()
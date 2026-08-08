
from hospital_mcp.database import SessionLocal
from hospital_mcp.doctor_model import DoctorModel


DOCTORS = [
    DoctorModel(
        id="D001",
        name="Dr. Ahmed Khan",
        specialty="Cardiology",
        experience_years=12,
    ),
    DoctorModel(
        id="D002",
        name="Dr. Sara Ali",
        specialty="Neurology",
        experience_years=8,
    ),
    DoctorModel(
        id="D003",
        name="Dr. Hassan Malik",
        specialty="Cardiology",
        experience_years=15,
    ),
    DoctorModel(
        id="D004",
        name="Dr. Ayesha Noor",
        specialty="Dermatology",
        experience_years=6,
    ),
]


def main() -> None:
    with SessionLocal() as session:
        session.add_all(DOCTORS)
        session.commit()

    print(f"Inserted {len(DOCTORS)} doctors.")


if __name__ == "__main__":
    main()
    
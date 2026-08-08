from hospital_mcp.database import Base, engine
from hospital_mcp.doctor_model import DoctorModel


def main() -> None:
    Base.metadata.create_all(engine)
    print("Database tables created.")


if __name__ == "__main__":
    main()

from hospital_mcp.appointments import book_appointment, search_available_slots
from hospital_mcp.billing import calculate_estimated_bill, get_patient_balance
from hospital_mcp.doctors import get_doctor, get_doctor_availability, search_doctors
from hospital_mcp.hospital_store import reset_demo_state
from hospital_mcp.patients import get_patient, get_patient_appointments, get_patient_records


def main() -> None:
    reset_demo_state()

    cardiologists = search_doctors("cardiology")
    patient = get_patient("P001")
    selected_doctor = get_doctor("D001")
    available_slots = search_available_slots("D001")
    booking = book_appointment("P001", "D001", available_slots[0])
    estimate = calculate_estimated_bill("D001")
    balance = get_patient_balance("P001")

    print("Cardiologists:")
    for cardiologist in cardiologists:
        print(cardiologist)

    print("\nDoctor D001:")
    print(selected_doctor)

    print("\nDoctor D001 availability:")
    print(get_doctor_availability("D001"))

    print("\nPatient P001:")
    print(patient)

    print("\nPatient P001 records:")
    print(get_patient_records("P001"))

    print("\nPatient P001 appointments:")
    print(get_patient_appointments("P001"))

    print("\nAppointment booking:")
    print(booking)

    print("\nEstimated bill:")
    print(estimate)

    print("\nPatient balance:")
    print(balance)


if __name__ == "__main__":
    main()
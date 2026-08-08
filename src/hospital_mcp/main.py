
from doctors import get_doctor, search_doctors


def main() -> None:
    cardiologists = search_doctors("cardiology")

    print("Cardiologists:")
    for doctor in cardiologists:
        print(doctor)

    print("\nDoctor D001:")
    print(get_doctor("D001"))


if __name__ == "__main__":
    main()
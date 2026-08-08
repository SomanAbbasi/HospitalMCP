from hospital_mcp.doctors import get_doctor, search_doctors


def test_search_doctors_by_specialty() -> None:
    doctors = search_doctors("Cardiology")

    assert len(doctors) == 2
    assert doctors[0]["id"] == "D001"
    assert doctors[1]["id"] == "D003"


def test_search_doctors_is_case_insensitive() -> None:
    doctors = search_doctors("CARDIOLOGY")

    assert len(doctors) == 2


def test_get_doctor_by_id() -> None:
    doctor = get_doctor("D001")

    assert doctor is not None
    assert doctor["name"] == "Dr. Ahmed Khan"


def test_get_unknown_doctor_returns_none() -> None:
    doctor = get_doctor("D999")

    assert doctor is None
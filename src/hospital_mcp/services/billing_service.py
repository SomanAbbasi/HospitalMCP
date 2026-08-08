from hospital_mcp.hospital_store import (
    BILLING_SERVICES,
    InvoiceRecord,
    copy_invoice,
    get_doctor_record,
    get_invoice_record,
    get_patient_record,
    next_invoice_id,
)


def _consultation_fee(specialty: str) -> float:
    for service in BILLING_SERVICES:
        if service["name"] == "Consultation":
            fees = service["fees"]
            return float(fees[specialty])

    raise ValueError("Consultation fees are not configured.")


def _lab_fee() -> float:
    for service in BILLING_SERVICES:
        if service["name"] == "Lab Add-On":
            return float(service["fee"])

    return 0.0


def calculate_estimated_bill(doctor_id: str, include_lab: bool = False) -> dict:
    doctor = get_doctor_record(doctor_id)

    if doctor is None:
        raise ValueError(f"Doctor '{doctor_id}' was not found.")

    items = [
        {
            "description": f"{doctor['specialty']} consultation",
            "amount": _consultation_fee(doctor["specialty"]),
        }
    ]

    if include_lab:
        items.append(
            {
                "description": "Lab add-on",
                "amount": _lab_fee(),
            }
        )

    total = round(sum(item["amount"] for item in items), 2)

    return {
        "doctor_id": doctor["id"],
        "specialty": doctor["specialty"],
        "items": items,
        "total": total,
        "currency": "USD",
    }


def create_invoice_for_appointment(
    appointment_id: str,
    patient_id: str,
    doctor_id: str,
) -> dict:
    estimate = calculate_estimated_bill(doctor_id)
    invoice_id = next_invoice_id()
    invoice: InvoiceRecord = {
        "id": invoice_id,
        "patient_id": patient_id,
        "appointment_id": appointment_id,
        "items": estimate["items"],
        "total": estimate["total"],
        "paid": False,
    }

    from hospital_mcp.hospital_store import INVOICES

    INVOICES[invoice_id] = invoice

    return copy_invoice(invoice)


def get_invoice(invoice_id: str) -> dict | None:
    invoice = get_invoice_record(invoice_id)

    if invoice is None:
        return None

    return copy_invoice(invoice)


def get_patient_balance(patient_id: str) -> dict:
    patient = get_patient_record(patient_id)

    if patient is None:
        raise ValueError(f"Patient '{patient_id}' was not found.")

    from hospital_mcp.hospital_store import INVOICES

    invoices = [
        copy_invoice(invoice)
        for invoice in INVOICES.values()
        if invoice["patient_id"] == patient["id"]
    ]

    outstanding_balance = round(
        sum(invoice["total"] for invoice in invoices if not invoice["paid"]),
        2,
    )

    return {
        "patient_id": patient["id"],
        "outstanding_balance": outstanding_balance,
        "currency": "USD",
        "invoices": invoices,
    }
# Hospital MCP Architecture And Progress

This repository currently has a clean in-memory hospital slice that is runnable end-to-end:

- doctors, patients, appointments, and billing all work from one shared demo store
- the package entrypoint runs locally
- the MCP server exposes tools, resources, and prompts for the full demo flow
- the MCP client can discover the server and exercise the whole flow
- PostgreSQL scaffolding still exists, but it is intentionally not wired into the active runtime yet

## What Is Implemented Today

### Shared demo store

The shared demo state lives in [src/hospital_mcp/hospital_store.py](src/hospital_mcp/hospital_store.py).

It contains:

- synthetic doctors
- synthetic patients
- sample medical records
- appointment state
- invoice state
- seed data for specialties, departments, and billing services

### Doctor flow

The doctor public API lives in [src/hospital_mcp/doctors.py](src/hospital_mcp/doctors.py).

It provides:

- `search_doctors(specialty)`
- `get_doctor(doctor_id)`
- `get_doctor_availability(doctor_id)`

### Patient flow

The patient public API lives in [src/hospital_mcp/patients.py](src/hospital_mcp/patients.py).

It provides:

- `get_patient(patient_id)`
- `get_patient_records(patient_id)`
- `get_patient_appointments(patient_id)`

### Appointment flow

The appointment public API lives in [src/hospital_mcp/appointments.py](src/hospital_mcp/appointments.py).

It provides:

- `search_available_slots(doctor_id)`
- `book_appointment(patient_id, doctor_id, scheduled_at)`
- `cancel_appointment(appointment_id)`
- `reschedule_appointment(appointment_id, new_scheduled_at)`

### Billing flow

The billing public API lives in [src/hospital_mcp/billing.py](src/hospital_mcp/billing.py).

It provides:

- `calculate_estimated_bill(doctor_id, include_lab=False)`
- `get_invoice(invoice_id)`
- `get_patient_balance(patient_id)`

### Runnable entrypoints

The package entrypoint is [src/hospital_mcp/main.py](src/hospital_mcp/main.py).

It resets the demo state and walks through:

- doctor search
- patient lookup
- appointment booking
- billing estimate
- patient balance

The package launcher is [src/hospital_mcp/__main__.py](src/hospital_mcp/__main__.py), so this works:

- `uv run python -m hospital_mcp`

The root [main.py](main.py) forwards to the package entrypoint.

### MCP server

The server lives in [src/hospital_mcp/mcp_server.py](src/hospital_mcp/mcp_server.py).

It uses `MCPServer` from the installed SDK and registers:

- doctor tools
- patient tools
- appointment tools
- billing tools
- hospital resources
- doctor and appointment prompts

### MCP client

The client lives in [src/hospital_mcp/mcp_client.py](src/hospital_mcp/mcp_client.py).

It launches the server, lists capabilities, reads resources, renders prompts, and calls the full demo workflow.

## Current File Roles

- [src/hospital_mcp/hospital_store.py](src/hospital_mcp/hospital_store.py): single source of truth for demo data and mutable state.
- [src/hospital_mcp/doctors.py](src/hospital_mcp/doctors.py): public doctor facade.
- [src/hospital_mcp/patients.py](src/hospital_mcp/patients.py): public patient facade.
- [src/hospital_mcp/appointments.py](src/hospital_mcp/appointments.py): public appointment facade.
- [src/hospital_mcp/billing.py](src/hospital_mcp/billing.py): public billing facade.
- [src/hospital_mcp/services/doctor_service.py](src/hospital_mcp/services/doctor_service.py): doctor business logic over the demo store.
- [src/hospital_mcp/services/patient_service.py](src/hospital_mcp/services/patient_service.py): patient business logic over the demo store.
- [src/hospital_mcp/services/appointment_service.py](src/hospital_mcp/services/appointment_service.py): appointment business logic over the demo store.
- [src/hospital_mcp/services/billing_service.py](src/hospital_mcp/services/billing_service.py): billing business logic over the demo store.
- [src/hospital_mcp/mcp_server.py](src/hospital_mcp/mcp_server.py): MCP server and registered tools/resources/prompts.
- [src/hospital_mcp/mcp_client.py](src/hospital_mcp/mcp_client.py): MCP client smoke test and discovery demo.
- [src/hospital_mcp/config.py](src/hospital_mcp/config.py): environment-backed settings.
- [src/hospital_mcp/database.py](src/hospital_mcp/database.py): SQLAlchemy engine/session setup for the later PostgreSQL phase.
- [src/hospital_mcp/doctor_model.py](src/hospital_mcp/doctor_model.py): SQLAlchemy doctor model for the later PostgreSQL phase.
- [scripts/create_tables.py](scripts/create_tables.py): future database table creation script.
- [scripts/seed_doctors.py](scripts/seed_doctors.py): future PostgreSQL seed script.

## Verified Commands

These commands should work once the code is validated again:

- `uv run python -m hospital_mcp.main`
- `uv run python -m hospital_mcp`
- `uv run python src\hospital_mcp\mcp_client.py`
- `uv run pytest`

## What Was Fixed Earlier

The first checkpoint fixed the package wiring and MCP SDK mismatch:

- package-relative imports were changed to package imports
- `MCPServer` replaced the unavailable `fastmcp` import path
- the client was updated to the installed SDK attribute names

## What Still Belongs To Future Phases

The incremental roadmap still makes sense, but these pieces should be added only when the phase needs them:

- PostgreSQL-backed repositories and persistence wiring
- Gemini integration
- LangGraph orchestration
- auth and RBAC
- remote streamable HTTP transport
- production hardening

## Suggested Next Step

The next real build step is to replace the in-memory demo store with PostgreSQL-backed repositories while keeping the same public facade and MCP tool names.
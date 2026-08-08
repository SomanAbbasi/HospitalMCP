# Hospital MCP Architecture And Progress

This repository is currently at a working checkpoint for the early hospital MCP flow:

- In-memory doctor data exists.
- A runnable package entrypoint exists.
- The MCP server exposes doctor search, doctor lookup, doctor availability, one resource layer, and one prompt.
- The MCP client can discover the server, list tools/resources/prompts, read a resource, and call tools successfully.
- PostgreSQL models and database scaffolding already exist, but they are not yet wired into the active tool path.

## What Is Implemented Today

### 1. Doctor domain in memory

The core domain lives in [src/hospital_mcp/doctors.py](src/hospital_mcp/doctors.py).

It currently provides:

- `search_doctors(specialty)`
- `get_doctor(doctor_id)`
- `get_doctor_availability(doctor_id)`

The data is a small synthetic in-memory list so the system stays simple and runnable.

### 2. Runnable application entrypoints

The package entrypoint is [src/hospital_mcp/main.py](src/hospital_mcp/main.py).

It demonstrates the basic backend behavior by calling `search_doctors()` and `get_doctor()`.

The package also has [src/hospital_mcp/__main__.py](src/hospital_mcp/__main__.py), so this works:

- `uv run python -m hospital_mcp`

The root [main.py](main.py) now forwards to the package entrypoint.

### 3. MCP server

The server lives in [src/hospital_mcp/mcp_server.py](src/hospital_mcp/mcp_server.py).

It uses the installed `mcp.server.mcpserver.MCPServer` API and registers:

- `search_hospital_doctors`
- `get_hospital_doctor`
- `get_hospital_doctor_availability`
- `hospital://specialties`
- `hospital://info`
- `doctor_consultation`

The server currently runs over stdio, which keeps the setup local and simple.

### 4. MCP client

The client lives in [src/hospital_mcp/mcp_client.py](src/hospital_mcp/mcp_client.py).

It launches the server, lists capabilities, reads a resource, renders a prompt, and calls the doctor tools.

## Current File Roles

- [src/hospital_mcp/doctors.py](src/hospital_mcp/doctors.py): domain logic and synthetic doctor data.
- [src/hospital_mcp/main.py](src/hospital_mcp/main.py): local Python demo entrypoint.
- [src/hospital_mcp/__main__.py](src/hospital_mcp/__main__.py): package launcher for `python -m hospital_mcp`.
- [src/hospital_mcp/mcp_server.py](src/hospital_mcp/mcp_server.py): MCP server and registered tools/resources/prompts.
- [src/hospital_mcp/mcp_client.py](src/hospital_mcp/mcp_client.py): MCP client smoke test and discovery demo.
- [src/hospital_mcp/config.py](src/hospital_mcp/config.py): environment-backed settings.
- [src/hospital_mcp/database.py](src/hospital_mcp/database.py): SQLAlchemy engine/session setup.
- [src/hospital_mcp/doctor_model.py](src/hospital_mcp/doctor_model.py): SQLAlchemy doctor table model.
- [src/hospital_mcp/services/doctor_service.py](src/hospital_mcp/services/doctor_service.py): PostgreSQL-facing doctor query helper, not yet wired into MCP.
- [scripts/create_tables.py](scripts/create_tables.py): creates database tables.
- [scripts/seed_doctors.py](scripts/seed_doctors.py): seeds PostgreSQL doctor rows.

## Verified Commands

These commands currently work:

- `uv run python -m hospital_mcp.main`
- `uv run python -m hospital_mcp`
- `uv run python src\hospital_mcp\mcp_client.py`
- `uv run pytest`

## What Was Fixed In This Checkpoint

The repo previously had two practical issues:

- package-relative imports were written as top-level imports like `from doctors import ...`
- the MCP server used `mcp.server.fastmcp`, which is not available in the installed SDK here

The current checkpoint fixes both by:

- switching imports to `hospital_mcp.doctors`
- using `MCPServer` from the installed `mcp.server.mcpserver` package
- adjusting the client to the installed SDK's snake_case attributes

## What Still Belongs To Future Phases

The incremental roadmap still makes sense, but these pieces should be added only when the phase needs them:

- PostgreSQL-backed doctor repository wiring
- patient domain
- appointment booking and conflict handling
- billing
- resources expansion
- prompts expansion
- Gemini client integration
- LangGraph orchestration
- auth and RBAC
- remote transport and production hardening

## Suggested Next Step

Phase 4 is the natural next build target: replace the in-memory doctor reads with PostgreSQL-backed service calls while keeping the MCP surface stable.
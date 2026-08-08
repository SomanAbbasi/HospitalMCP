import pytest

from hospital_mcp.hospital_store import reset_demo_state


@pytest.fixture(autouse=True)
def reset_hospital_state() -> None:
    reset_demo_state()
    yield
    reset_demo_state()
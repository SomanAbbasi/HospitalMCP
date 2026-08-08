from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from hospital_mcp.database import Base


class DoctorModel(Base):
    __tablename__ = "doctors"

    id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    specialty: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    experience_years: Mapped[int] = mapped_column(
        nullable=False,
    )
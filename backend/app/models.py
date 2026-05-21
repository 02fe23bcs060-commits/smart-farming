from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    inputs: Mapped[list["FarmInput"]] = relationship(back_populates="farmer")
    recommendations: Mapped[list["RecommendationHistory"]] = relationship(
        back_populates="farmer"
    )


class FarmInput(Base):
    __tablename__ = "farm_inputs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"), index=True)
    soil_type: Mapped[str] = mapped_column(String(50))
    season: Mapped[str] = mapped_column(String(30))
    temperature_c: Mapped[float] = mapped_column(Float)
    water_availability: Mapped[str] = mapped_column(String(30))
    land_size_acres: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    farmer: Mapped["Farmer"] = relationship(back_populates="inputs")


class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"), index=True)
    farm_input_id: Mapped[int | None] = mapped_column(
        ForeignKey("farm_inputs.id"), nullable=True
    )
    crop_recommendations: Mapped[dict] = mapped_column(JSONB)
    fertilizer_plan: Mapped[dict] = mapped_column(JSONB)
    irrigation_schedule: Mapped[dict] = mapped_column(JSONB)
    weather_alerts: Mapped[dict] = mapped_column(JSONB)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    farmer: Mapped["Farmer"] = relationship(back_populates="recommendations")

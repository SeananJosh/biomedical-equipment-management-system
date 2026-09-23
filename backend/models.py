from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from database import Base
from sqlalchemy.orm import relationship
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)
    serial_number = Column(String, unique=True, index=True)
    department = Column(String, index=True)
    status = Column(String, index=True)

    maintenance_records = relationship(
        "MaintenanceRecord",
        back_populates="equipment",cascade="all,delete-orphan"
    )
class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    description = Column(String, nullable=False)
    equipment = relationship("Equipment", back_populates="maintenance_records")
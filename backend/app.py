from fastapi import FastAPI, Depends,HTTPException,status
from database import get_db
from models import Equipment,MaintenanceRecord
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
app = FastAPI()
# Equipment update feature branch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class EquipmentCreate(BaseModel):
    name: str
    model: str
    serial_number: str
    department: str
    status: Literal["available", "maintenance", "unavailable"]
class EquipmentResponse(BaseModel):
    id: int
    name: str
    model: str | None=None
    serial_number: str | None=None
    department: str | None=None
    status: str

    model_config = ConfigDict(from_attributes=True)
class MaintenanceResponse(BaseModel):
    id: int
    equipment_id: int
    description: str

    model_config = ConfigDict(from_attributes=True)
class EquipmentCreateResponse(BaseModel):
    message: str
    equipment: EquipmentResponse
class EquipmentUpdate(BaseModel):
    name: str | None = None
    model: str | None = None
    serial_number: str | None = None
    department: str | None = None
    status: Literal[
        "available",
        "maintenance",
        "unavailable"
    ] | None = None

class MaintenanceCreate(BaseModel):
    description: str
class EquipmentWithMaintenanceResponse(BaseModel):
    id: int
    name: str
    status: str
    model: str | None=None
    serial_number: str | None=None
    department: str | None=None
    maintenance_records: list[MaintenanceResponse]
    model_config = ConfigDict(from_attributes=True)
class EquipmentMaintenanceResponse(BaseModel):
    name: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)
class EquipmentMaintenanceCountResponse(BaseModel):
    name: str
    maintenance_count: int
@app.get("/")
def home():
    return {"message": "Biomedical Equipment Management System"}


@app.get("/equipment",response_model=list[EquipmentResponse])
def get_equipment(db: Session=Depends(get_db)):

    equipment = db.query(Equipment).all()

    return equipment

@app.get("/equipment/{equipment_id}",response_model=EquipmentWithMaintenanceResponse)
def get_equipment_by_id(equipment_id: int, db: Session=Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@app.post(
    "/equipment",
    response_model=EquipmentCreateResponse,
    status_code=201
)
def add_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db)
):
    new_equipment = Equipment(
        name=equipment.name,
        model=equipment.model,
        serial_number=equipment.serial_number,
        department=equipment.department,
        status=equipment.status
    )

    db.add(new_equipment)
    try:
        db.commit()
        db.refresh(new_equipment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Serial number already exists")

    return {
        "message": "Equipment added successfully",
        "equipment": new_equipment
    }
@app.put(
    "/equipment/{equipment_id}",
    response_model=EquipmentCreateResponse
)
def update_equipment(
    equipment_id: int,
    equipment: EquipmentCreate,
    db: Session = Depends(get_db)
):
    equipment_to_update = db.query(Equipment).filter(
        Equipment.id == equipment_id
    ).first()

    if not equipment_to_update:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    equipment_to_update.name = equipment.name
    equipment_to_update.model = equipment.model
    equipment_to_update.serial_number = equipment.serial_number
    equipment_to_update.department = equipment.department
    equipment_to_update.status = equipment.status

    db.commit()
    db.refresh(equipment_to_update)

    return {
        "message": "Equipment updated successfully",
        "equipment": equipment_to_update
    }
@app.delete("/equipment/{equipment_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: int,db: Session=Depends(get_db)):
    
    equipment=db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment:
        db.delete(equipment)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Equipment not found")
@app.patch(
    "/equipment/{equipment_id}",
    response_model=EquipmentCreateResponse
)
def partial_update_equipment(
    equipment_id: int,
    equipment: EquipmentUpdate,
    db: Session = Depends(get_db)
):
    equipment_to_update = db.query(Equipment).filter(
        Equipment.id == equipment_id
    ).first()

    if not equipment_to_update:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    if equipment.name is not None:
        equipment_to_update.name = equipment.name

    if equipment.model is not None:
        equipment_to_update.model = equipment.model

    if equipment.serial_number is not None:
        equipment_to_update.serial_number = equipment.serial_number

    if equipment.department is not None:
        equipment_to_update.department = equipment.department

    if equipment.status is not None:
        equipment_to_update.status = equipment.status

    db.commit()
    db.refresh(equipment_to_update)

    return {
        "message": "Equipment updated successfully",
        "equipment": equipment_to_update
    }
@app.post("/equipment/{equipment_id}/maintenance",status_code=201,response_model=MaintenanceResponse)
def add_maintenance(equipment_id: int, maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    new_record = MaintenanceRecord(
        equipment_id=equipment_id,
        description=maintenance.description
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@app.get("/equipment/{equipment_id}/maintenance",response_model=list[MaintenanceResponse])
def get_maintenance(equipment_id: int,db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    maintenance_records = db.query(MaintenanceRecord).filter(MaintenanceRecord.equipment_id == equipment_id).all()

    return maintenance_records
@app.get("/maintenance/{maintenance_id}",response_model=MaintenanceResponse)
def get_maintenance_record(maintenance_id: int, db: Session = Depends(get_db)):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == maintenance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return record
@app.put("/maintenance/{maintenance_id}",response_model=MaintenanceResponse)
def update_maintenance_record(maintenance_id: int, maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == maintenance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    record.description = maintenance.description
    db.commit()
    db.refresh(record)

    return record
@app.delete("/maintenance/{maintenance_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance_record(maintenance_id: int, db: Session = Depends(get_db)):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == maintenance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    db.delete(record)
    db.commit()
    return
@app.get("/equipment-with-maintenance",response_model=list[EquipmentMaintenanceResponse])
def get_equipment_with_maintenance(db: Session = Depends(get_db)):

    results = (
        db.query(Equipment.name, MaintenanceRecord.description)
        .join(
            MaintenanceRecord,
            Equipment.id == MaintenanceRecord.equipment_id
        )
        .all()
    )

    return results
@app.get("/equipment/{equipment_id}/maintenance-details",response_model=list[EquipmentMaintenanceResponse])
def get_equipment_maintenance_details(equipment_id: int, db: Session = Depends(get_db)):

    results = (
        db.query(Equipment.name, MaintenanceRecord.description)
        .join(
            MaintenanceRecord,
            Equipment.id == MaintenanceRecord.equipment_id
        )
        .filter(Equipment.id == equipment_id)
        .all()
    )

    return results
@app.get("/all-equipment-maintenance",response_model=list[EquipmentMaintenanceResponse])
def get_all_equipment_maintenance(db: Session = Depends(get_db)):

    results = (
        db.query(Equipment.name, MaintenanceRecord.description)
        .outerjoin(
            MaintenanceRecord,
            Equipment.id == MaintenanceRecord.equipment_id
        )
        .all()
    )

    return results
@app.get("/equipment-maintenance-count",response_model=list[EquipmentMaintenanceCountResponse])
def get_equipment_maintenance_count(db: Session = Depends(get_db)):

    results = (
        db.query(
            Equipment.name,
            func.count(MaintenanceRecord.id).label("maintenance_count")
        )
        .outerjoin(
            MaintenanceRecord,
            Equipment.id == MaintenanceRecord.equipment_id
        )
        .group_by(Equipment.name)
        .all()
    )

    return results
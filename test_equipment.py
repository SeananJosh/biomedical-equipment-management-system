from backend.database import SessionLocal
from backend.models import Equipment, MaintenanceRecord

db = SessionLocal()

record = db.query(MaintenanceRecord).filter(
    MaintenanceRecord.id == 1
).first()

print("Maintenance:", record.description)
print("Equipment:", record.equipment.name)
db.close()
from backend.database import SessionLocal
from backend.models import Equipment

db = SessionLocal()

equipment = db.query(Equipment).all()

for item in equipment:
    print(item.id, item.name, item.status)

db.close()
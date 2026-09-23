from database import Base,engine
from backend.models import Equipment

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
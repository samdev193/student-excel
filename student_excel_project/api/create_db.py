from connect_db import Base, engine
from models import Student
print('Creating database ....')

Base.metadata.create_all(engine)

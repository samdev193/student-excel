from connect_db import Base
from sqlalchemy import String, Boolean, Integer, Column

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    tuition_paid = Column(Boolean, nullable=False)

    def __repr__(self):
        return f'<Student name={self.first_name} {self.last_name}, id= {self.id}>qu'


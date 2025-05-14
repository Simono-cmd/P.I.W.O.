from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy.orm import validates

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Validations
    @validates('id')
    def validate_id(self, key, value):
        if value < 0:
            raise ValueError("ID must not be lesser than 0")
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

    # Relationships
    grades = relationship("Grade", backref="subject")
    attendances = relationship("Attendance", backref="subject")
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
import datetime

class Base(DeclarativeBase):
    pass

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    type = Column(String)
    adopted = Column(Boolean, default=False)

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

class AdoptionRequest(Base):
    __tablename__ = 'adoption_requests'
    id = Column(Integer, primary_key=True)
    person = relationship("Person")
    pet = relationship("Pet")
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=True)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=True)
    status = Column(String)
    date = Column(Date, default=datetime.date.today)
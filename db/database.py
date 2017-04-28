from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Persons(Base):
    def __init__(self, id, full_name, person_title, accomodate, allocation):
        self.id = id
        self.full_name = full_name
        self.person_title = person_title
        self.acccomodate = accomodate
        self.allocation = allocation

    __tablename__ = 'Persons'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(500), nullable=False)
    person_title = Column(String(500), nullable=False)
    accomodated = Column(String(500), nullable=True)
    allocation = Column(String(500), nullable=True)


class Rooms(Base):
    def __init__(self, room_name, room_type, max_capacity, occupants):
        self.room_name = room_name
        self.room_type = room_type
        self.max_capacity = max_capacity
        self.occupants = occupants

    __tablename__ = 'Rooms'

    id = Column(Integer, primary_key=True)
    room_name = Column(String(500), nullable=False)
    room_type = Column(String(500), nullable=False)
    max_capacity = Column(Integer, nullable=False)
    occupants = Column(String, nullable=True)


class Allocations(Base):
    def __init__(self, full_name, office_name, livingsp_name):
        self.full_name = full_name
        self.office_name = office_name
        self.livingsp_name = livingsp_name

    __tablename__ = 'Allocations'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(500), nullable=False)
    office_name = Column(String(500), nullable=True)
    livingsp_name = Column(String(500), nullable=True)



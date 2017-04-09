from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

BASE = declarative_base()

class Persons(BASE):

    __tablename__ = 'Persons'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(500), nullable=False)
    person_title = Column(String(500), nullable=False)

class Rooms(BASE):

    __tablename__ = 'Rooms'

    id = Column(Integer, primary_key=True)
    room_name = Column(String(500), nullable=False)
    room_type = Column(String(500), nullable=False)
    max_capacity = Column(Integer, nullable=False)
    capacity_occupied = Column(Integer, nullable=True)


class Allocations(BASE):

    __tablename__ = 'Allocations'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(500), nullable=False)
    office_name = Column(String(500), nullable=True)
    livingsp_name = Column(String(500), nullable=True)


ENGINE = create_engine('sqlite:///amity.db')
BASE.metadata.create_all(ENGINE)

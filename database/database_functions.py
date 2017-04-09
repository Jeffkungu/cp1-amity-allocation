from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Persons, Rooms, Allocations, BASE

ENGINE = create_engine('sqlite:///amity.db')

BASE.metadata.create_all(ENGINE)
DBSESSION = sessionmaker(bind=ENGINE)
SESSIONS = DBSESSION()

def get_persons():
    #Getting all persons in the data base and adding them to a persons dictionary
    person = SESSIONS.query(Persons).all()
    persons_dct = {}
    for persons in person:
        persons_dct.update({person.full_name:person.person_title})

    return persons_dct

def get_rooms():
    #Getting all the rooms in the data base and adding them to a rooms dictionary
    room = SESSIONS.query(Rooms).all()
    rooms_dct = {}
    for rooms in room:
        rooms_dct.update({room.room_name:room.room_type})

    return rooms_dct

def get_allocations():
    #Getting all the allocations from database and adding them to an allocations dictionary
    allocations = SESSIONS.query(Allocations).all()
    allocations_dct = {}
    for allocation in allocations:
        allocations_dct.update({allocations.full_name:[allocations.office_name, allocations.livingsp_name]})

    return allocations_dct


def add_person(full_name, person_title):
    # Adding a person to the database
    newperson = Persons()
    SESSIONS.add(newperson)
    SESSIONS.commit()

def add_room(room_name, room_type, max_capacity):
    #Adding a room to the database
    newuser = Rooms()
    SESSIONS.add(newuser)
    SESSIONS.commit()

def allocate_room(room_name, person_type):
    #Adding a person to database
    newallocation = SESSIONS.query(Rooms).filter_by(room_name = room_name).one()
    newallocation.capacity_occupied +=1
    SESSIONS.add(newallocation)
    SESSIONS.commit()

def add_allocation(person_name, office_name, livingspace_name):
    newallocation = Allocations()
    SESSIONS.add(newallocation)
    SESSIONS.commit()

def edit_allocation(p_name, office_name, livingspaces_name):
    rellocation = SESSIONS.query(Rooms).filter_by(full_name = full_name).one()
    rellocation.office_name = office_name
    rellocation.livingsp_name = livingsp_name

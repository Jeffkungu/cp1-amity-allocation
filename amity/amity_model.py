import random
import os
from termcolor import colored
from sqlalchemy import create_engine
from person.persons import Person, Fellow, Staff
from room.rooms import Room, LivingSpace, Office
from db.database import Base, Persons, Rooms, Allocations
from sqlalchemy.orm import sessionmaker


class Amity(object):
    def __init__(self):
        self.existing_rooms = []
        self.every_person = []

    def create_room(self, room_name, room_type):
        room = [r.room_name for r in self.existing_rooms]
        if room_name.upper() in room:
            return ("Room %s already exists" %room_name)
        else:
            if room_type.upper() == "LIVING SPACE":
                self.existing_rooms.append(LivingSpace(room_name.upper()))
                return "Living Space successfully created"
            elif room_type.upper() == "OFFICE":
                  self.existing_rooms.append(Office(room_name.upper()))
                  return "Office successfully created"
            else:
                if room_type.upper() != str or room_type.upper() not in ['OFFICE', 'LIVING SPACE']:
                    return "Invalid room type, should be LIVING SPACE or OFFICE"

    def add_person(self, first_name, last_name, person_title, accomodation):
        person_title = person_title.upper()
        full_name = first_name + " " + last_name
        if type(first_name) != str or type(last_name) != str:
            return "Invalid name. Name should be letters"
        else:
            if person_title.upper() not in ["STAFF", "FELLOW"]:
                return "Invalid role, should be STAFF or FELLOW"
            elif accomodation == "N" and person_title == "FELLOW":
                fellow = Fellow(first_name, last_name)
                self.every_person.append(fellow)
                return ("%s successfully added"% full_name, fellow.identifier)
            elif accomodation == "N" and person_title == "STAFF":
                staff = Staff(first_name, last_name)
                self.every_person.append(staff)
                return ("%s successfully added"% full_name, staff.identifier)
            elif accomodation == "Y" and person_title == "FELLOW":
                 fellow = Fellow(first_name, last_name)
                 self.every_person.append(fellow)
                 return ("%s successfully added"% full_name, fellow.identifier)
            else:
                if accomodation == "Y" and person_title == "STAFF":
                    return "Invalid input, staff can not get accomodation"

    def allocate_room(self, id_no, accomodation):
        livingsp_available = [l for l in self.existing_rooms if l.room_type == "LIVING SPACE"
                               and l.max_capacity > len(l.occupants)]
        offices_available = [o for o in self.existing_rooms if o.room_type == "OFFICE"
                             and o.max_capacity > len(o.occupants)]
        person = [person for person in self.every_person if person.identifier == id_no]

        if len(livingsp_available) > 0 and len(offices_available) > 0:
            living_space = random.choice(list(livingsp_available))
            office = random.choice(list(offices_available))
            if person[0].person_title.upper() == "STAFF":
                if accomodation == "Y":
                    office.occupants.append(person[0])
                    person[0].allocation = office.room_name
                    return ("%s has been allocated an office only, staff can not get accomodation"% person[0].first_name)
                elif accomodation == "N":
                    office.occupants.append(person[0])
                    person[0].allocation = office.room_name
                    return ("Successfull %s has been allocated an office."% person[0].first_name)
                else:
                    return "Invalid input, choice of accomodation should be Y or N"
            elif person[0].person_title.upper() == "FELLOW":
                if accomodation == "Y":
                   office.occupants.append(person[0])
                   living_space.occupants.append(person[0])
                   person[0].accomodated = living_space.room_name
                   person[0].allocation = office.room_name
                   return ("Successfull %s has been allocated an office and a living space."% person[0].first_name)
                elif accomodation == "N":
                    office.occupants.append(person[0])
                    person[0].allocation = office.room_name
                    return ("Successfull %s has been allocated an office."% person[0].first_name)
                else:
                    return "Invalid input, choice of accomodation should be Y or N"
            else:
                return "Invalid input, person title should be FELLOW or STAFF"        

        elif len(livingsp_available) == 0 and len(offices_available) > 0:
             office = random.choice(list(offices_available))
             if person[0].person_title.upper() == "STAFF":
                 if accomodation == "Y":
                     office.occupants.append(person[0])
                     person[0].allocation = office.room_name
                     return ("%s has been allocated an office only, staff can not get accomodation"% person[0].first_name)
                 elif accomodation == "N":
                      office.occupants.append(person[0])
                      person[0].allocation = office.room_name
                      return ("Successfull %s has been allocated an office."% person[0].first_name)
                 else:
                     return "Invalid input, choice of accomodation should be Y or N"
             elif person[0].person_title.upper() == "FELLOW":
                 if accomodation == "Y":
                       office.occupants.append(person[0])
                       person[0].allocation = office.room_name
                       return ("%s has been allocated an office only, there are no living spaces available"% person[0].first_name)
                 elif accomodation == "N":
                      office.occupants.append(person[0])
                      person[0].allocation = office.room_name
                      return ("Successful.%s has been allocated an office."% person[0].first_name)
                 else:
                     return "Invalid input, choice of accomodation should be Y or N"
             else:
                 return "Invalid input, person title should be FELLOW or STAFF"
         
        elif len(livingsp_available) > 0 and len(offices_available) == 0:
            living_space.occupants.append(person[0])
            if person[0].person_title.upper() == "STAFF":
                 if accomodation == "Y":
                     return "Failed, staffs can not get accomodation"
                 elif accomodation == "N":
                     return "Sorry. There are no offices available"
                 else:
                     return "Invalid input. Choice of accomodation should be Y or N"
            elif person[0].person_title.upper() == "FELLOW":
                if accomodation == "Y":
                    living_space.occupants.append(person[0])
                    person[0].living_space = living_space.room_name
                    return ("Successful. %s has been allocated living space only. \nThere are no offices available"% person[0].first_name)
                elif accomodation == "N":
                    return "Sorry. There are no offices available"
                else:
                    return "Invalid input. Choice of accomodation should be Y or N"
            else:
                return "Invalid input, person title should be FELLOW or STAFF"

        else:
            if len(livingsp_available) == 0 and len(offices_available) == 0:
                return "Sorry. There are no living space or offices available"

    def fetch_person(self, id_no):
        '''Gets you the person with all attributes attached to the person object.
           Gets the person using the Id assigned to the person'''
        identifiers = [person.identifier for person in self.every_person]
        if id_no in identifiers:
            person = [person for person in self.every_person if person.identifier == id_no]
            return person[0]
        else:
            return "Sorry, person does not exist"

    def fetch_room(self, name):
        '''Gets you the room with all the occupants present '''
        rooms = [room.room_name for room in self.existing_rooms]
        if name.upper() in rooms:
            fetched_room = [room for room in self.existing_rooms if room.room_name == name.upper()]
            return fetched_room[0]
        else:
            return "Sorry, room does not exist"                
        
    def reallocate_room(self, id_no, r_name):
        '''Rellocates a person to a new room. First it checks whether the person exists, and if the person exists in the list of occupants of a specific room.
           It then reallocates the person to a room if the person exists and is not in the list of occcupants of the room are reallocatig to'''
        person = self.fetch_person(id_no)
        title = person.person_title
        room = self.fetch_room(r_name)
        r_type = room.room_type

        if person == "Sorry, person does not exist":
            print ("Sorry, person does not exist")
            return "Sorry, person does not exist"
        elif room == "Sorry, room does not exist":
            print ("Sorry, room does not exist")
            return "Sorry, room does not exist"
        else:
            room.occupants.append(person)
            for r in self.existing_rooms:
                occupant_found = [ p for p in r.occupants if p.identifier == id_no]
                if len(occupant_found)>0:
                    r.occupants.remove(person) 
                return ("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name))

    def print_allocations(self, file_name=None):
        '''
        Prints all allocations.
        '''
        for room in self.existing_rooms:
            print (room.room_name)
            names_of_people = [person.first_name for person in room.occupants]
            print (",".join(names_of_people))

        if file_name  == None:
            return "Successful"
        else:
            file = open(file_name, 'w')
            for room in self.existing_rooms:
                file.write(room.room_name+"\n")
                file.write('-------------------------------------------------'+ "\n")
                names_of_people = [person.full_name for person in room.occupants]
                file.write(",".join(names_of_people)+"\n")
            file.close()


    def print_unallocated(self, file_name=None):
        '''
        Prints all unallocated.
        '''
        unallocated = []
        for person in self.every_person:
            if person.person_title.upper() == "FELLOW":
                if person.allocation == None:
                    a = [person.identifier, person.first_name]
                    unallocated.append(a)
                elif person.accomodated == None:
                    a = [person.identifier, person.first_name]
                    unallocated.append(a) 
            else:
                if person.person_title.upper() == "STAFF":
                    if person.allocation == None:
                        a = [person.identifier, person.first_name]
                        unallocated.append(a)
        print (unallocated)
        return "Successfully"

    # def load_people(self, file_name):
    #     try:
    #         file_object = open(file_name, 'r')
    #     except:
    #         return 'Wrong file'
    #     else:
    #         for line in file_object:
    #             objct = line.split()
    #             if len(objct) == 4:
    #                 self.add_person(object[0], object[1], object[2], object[3])
    #             elif len(object) == 3:
    #                 self.add_person(object[0], object[1], object[2], 'N')
    #             else:
    #                 return 'Wrong file'
    #         return 'People loaded succesfully'

        pass    

    def print_room(self, name):
        '''
        Prints a specific room with all the occupants within the room. 
        '''
        all_rooms = [room.room_name for room in self.existing_rooms]
        if name.upper() in all_rooms:
            specific_room = [room for room in self.existing_rooms if room.room_name == name.upper()]
            occupants_available = [person for person in specific_room[0].occupants]
            print (specific_room[0].room_name) 
            print ([person.first_name for person in occupants_available])
        else:
            return "Invalid room name. Room does not exist."


    def save_state(self, file_name=None):
        
        if file_name is None: 
            engine = create_engine('sqlite:///amity.db')
        else:
            engine = create_engine('sqlite:///' + file_name + '.db')
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)    
        Session = sessionmaker(bind=engine)
        session = Session()
        for room in self.existing_rooms:
            room_type = room.room_type
            room_name = room.room_name
            max_capacity = room.max_capacity
            str_occupants = [person.full_name for person in room.occupants]
            occupants_names = ".".join(str_occupants)

            room_details = Rooms(room_name, room_type, max_capacity, occupants_names)
            session.add(room_details)
        for person in self.every_person:
            if person.person_title.upper() == "FELLOW":
                id = person.identifier
                full_name = person.full_name
                person_title = person.person_title
                allocation = person.allocation
                accomodated = person.accomodated
                person_details = Persons(id, full_name, person_title, accomodated, allocation)
                session.add(person_details)
            else:
                id = person.identifier
                full_name = person.full_name
                person_title = person.person_title
                allocation = person.allocation
                accomodated = None
                person_details = Persons(id, full_name, person_title, accomodated, allocation)
                session.add(person_details)

        session.commit()        
        return "Data saved."

    def load_state(self, file_name=None):
        if file_name is None: 
            engine = create_engine('sqlite:///amity.db')
        else:
            engine = create_engine('sqlite:///' + file_name + '.db')
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)    
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            rooms = session.query(Rooms).all()
            persons = session.query(Persons).all()
        except:
            return ("Wrong file")

        for person in persons:
            if person.person_title == "FELLOW":
                person.full_name = person.full_name.split()
                fellow = Fellow(person.full_name[0], person.full_name[1])
                fellow.accomodated = person.accomodated
                fellow.allocation = person.allocation
                self.every_person.append(fellow) 
            else:
                person.full_name = person.full_name.split()
                staff = Staff(person.full_name[0], person.full_name[1])
                staff.allocation = person.allocation
                self.every_person.append(staff)     
        for room in rooms:
            if room.room_type == "OFFICE":
                office = Office(room.room_name)
                if len(room.occupants) != 0:
                    occupant_names = room.occupants.split(".")
                    for name in occupant_names:
                        the_person = [person for person in self.every_person if person.full_name == name]
                        if len(the_person) != 0:
                            office.occupants.append(the_person[0])

                self.existing_rooms.append(office)
            else:
                living_space = LivingSpace(room.room_name)
                if len(room.occupants) == 0:
                    occupant_names = room.occupants.split(".")
                    for name in occupant_names:
                        the_person = [person for person in self.every_person if person.full_name == name]
                        if len(the_person) != 0:
                            living_space.occupants.append(the_person[0])

                self.existing_rooms.append(living_space)


             

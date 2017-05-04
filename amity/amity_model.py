import random
import os
from termcolor import colored, cprint
from sqlalchemy import create_engine
from amity.persons import Person, Fellow, Staff
from amity.rooms import Room, LivingSpace, Office
from amity.database import Base, Persons, Rooms, Allocations
from sqlalchemy.orm import sessionmaker


class Amity(object):
    def __init__(self):
        self.existing_rooms = []
        self.every_person = []

    def create_room(self, room_name, room_type):
        rooms = [room.room_name for room in self.existing_rooms]
        if room_name.upper() in rooms:
            cprint("%s already exists" %room_name, "red")
            return "%s already exists" %room_name
        if room_type.upper() == "LIVINGSPACE":
            l_space = LivingSpace(room_name.upper())
            self.existing_rooms.append(l_space)
            cprint("Living Space successfully created", "cyan")
            return "Living Space successfully created"
        if room_type.upper() == "OFFICE":
            office = Office(room_name.upper())
            self.existing_rooms.append(office)
            cprint("Office successfully created", "cyan")
            return "Office successfully created"
        if room_type.upper() not in ['OFFICE', 'LIVINGSPACE']:
            cprint("Invalid room type, should be LIVING SPACE or OFFICE", "red")
            return "Invalid room type, should be LIVING SPACE or OFFICE"

    def add_person(self, first_name, last_name, person_title, accomodation):
        person_title = person_title.upper()
        full_name = first_name + " " + last_name
        if type(first_name) != str or type(last_name) != str:
            cprint("Error", "red")
            return "Invalid name. Name should be letters"
        if person_title.upper() not in ["STAFF", "FELLOW"]:
            cprint("Invalid role, should be STAFF or FELLOW", "red")
            return "Invalid role, should be STAFF or FELLOW"
        elif accomodation == "N" and person_title == "FELLOW":
            fellow = Fellow(first_name, last_name)
            self.every_person.append(fellow)
            cprint("%s successfully added"% full_name, "cyan") 
            cprint(fellow.identifier, "blue")
            return "Person successfully added"
        elif accomodation == "N" and person_title == "STAFF":
            staff = Staff(first_name, last_name)
            self.every_person.append(staff)
            cprint("%s successfully added"% full_name, "cyan")
            cprint(staff.identifier, "blue")
        elif accomodation == "Y" and person_title == "FELLOW":
                fellow = Fellow(first_name, last_name)
                self.every_person.append(fellow)
                cprint("%s successfully added"% full_name, "cyan")
                cprint(fellow.identifier, "blue")
        else:
            if accomodation == "Y" and person_title == "STAFF":
                cprint("Error", "red")
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
                    cprint("%s has been allocated an office only"% person[0].first_name, "blue")
                    return "Staff can not get accomodation"
                elif accomodation == "N":
                    office.occupants.append(person[0])
                    person[0].allocation = office.room_name
                    cprint("%s has been allocated an office."% person[0].first_name, "cyan")
                    return "Successfull person has been allocated an office."
                else:
                    cprint("Error", "red")
                    return "Invalid input, choice of accomodation should be Y or N"
            elif person[0].person_title.upper() == "FELLOW":
                if accomodation == "Y":
                   office.occupants.append(person[0])
                   living_space.occupants.append(person[0])
                   person[0].accomodated = living_space.room_name
                   person[0].allocation = office.room_name
                   cprint("%s has been allocated an office and a living space."% person[0].first_name, "cyan")
                   return "Successfull person has been allocated office and living space"
                elif accomodation == "N":
                    office.occupants.append(person[0])
                    person[0].allocation = office.room_name
                    cprint("%s has been allocated an office."% person[0].first_name, "cyan")
                    return "Successfull person has been allocated an office only."
                else:
                    cprint("Error", "red")
                    return "Invalid input, choice of accomodation should be Y or N"
            else:
                return cprint("Invalid input, person title should be FELLOW or STAFF", "red")        

        elif len(livingsp_available) == 0 and len(offices_available) > 0:
             office = random.choice(list(offices_available))
             if person[0].person_title.upper() == "STAFF":
                 if accomodation == "Y":
                     office.occupants.append(person[0])
                     person[0].allocation = office.room_name
                     cprint("%s has been allocated an office only"% person[0].first_name, "blue")
                     return "Staff can not get accomodation"
                 elif accomodation == "N":
                      office.occupants.append(person[0])
                      person[0].allocation = office.room_name
                      cprint("%s has been allocated an office."% person[0].first_name, "cyan")
                      return "Successfull person has been allocated an office."
                 else:
                     cprint("Error", "red")
                     return "Invalid input, choice of accomodation should be Y or N"
             elif person[0].person_title.upper() == "FELLOW":
                 if accomodation == "Y":
                       office.occupants.append(person[0])
                       person[0].allocation = office.room_name
                       return cprint("%s has been allocated an office only, there are no living spaces available"% person[0].first_name, "blue")
                 elif accomodation == "N":
                      office.occupants.append(person[0])
                      person[0].allocation = office.room_name
                      cprint("%s has been allocated an office."% person[0].first_name, "cyan")
                      return "Successfull person has been allocated an office only."
                 else:
                     cprint("Error", "red")
                     return "Invalid input, choice of accomodation should be Y or N"
             else:
                 cprint("Error", "red")
                 return "Invalid input, person title should be FELLOW or STAFF"
         
        elif len(livingsp_available) > 0 and len(offices_available) == 0:
            living_space.occupants.append(person[0])
            if person[0].person_title.upper() == "STAFF":
                 if accomodation == "Y":
                     cprint("Failed.", "red")
                     return "Staff can not get accomodation"
                 elif accomodation == "N":
                     return cprint("Sorry. There are no offices available", "red")
                 else:
                     cprint("Error", "red")
                     return "Invalid input, choice of accomodation should be Y or N"
            elif person[0].person_title.upper() == "FELLOW":
                if accomodation == "Y":
                    living_space.occupants.append(person[0])
                    person[0].living_space = living_space.room_name
                    return cprint("Successful. %s has been allocated living space only. \nThere are no offices available"% person[0].first_name, "blue")
                elif accomodation == "N":
                    return cprint("Sorry. There are no offices available", "red")
                else:
                    return cprint("Invalid input. Choice of accomodation should be Y or N", "red")
            else:
                return cprint("Invalid input, person title should be FELLOW or STAFF", "red")

        else:
            if len(livingsp_available) == 0 and len(offices_available) == 0:
                return cprint("Sorry. There are no living space or offices available", "red")

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
            return cprint("Sorry, person does not exist", "red")
        elif room == "Sorry, room does not exist":
            print ("Sorry, room does not exist")
            return cprint("Sorry, room does not exist", "red")
        else:
            room.occupants.append(person)
            for room in self.existing_rooms:
                occupant_found = [ p for p in room.occupants if p.identifier == id_no]
                if len(occupant_found)>0:
                    room.occupants.remove(person) 
            cprint("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name), "cyan")
            return "Successful"

    def print_allocations(self, file_name=None):
        '''
        Prints all allocations.
        '''
        output = ""
        if not self.existing_rooms:
            output = "There are no rooms in the system yet."
        else:
            output = "Rooms:\n" + ("="*10 + "\n")
            offices = [room for room in self.existing_rooms if room.room_type == "OFFICE"]
            for room in offices:
                output += "OFFICE:\n"
                output += room.room_name.upper() + "\n" + ("-" * 50 + "\n")
                for occupant in room.occupants:
                    output += "{}".format(occupant.full_name) + ", "

                output+="\n\n"

            living_space = [room for room in self.existing_rooms if room.room_type == "LIVING SPACE"]

            for room in living_space:
                output += "LIVING SPACE:\n"
                output += room.room_name.upper() + "\n" + ("-" * 50 + "\n")
                for occupant in room.occupants:
                    output += "{}".format(occupant.full_name) + ", "

                output+="\n\n"
                
        if file_name is None:
            return cprint(output, "cyan")
        if file_name[-4:] != ".txt":
            file_name += ".txt"
        with open(file_name, 'w+') as file:
            file.write(output)
            file.close()
            return cprint("Succesful!! The allocations have been saved in {}".format(file_name), "cyan")


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
        cprint(unallocated, "cyan")
        return "Successfull"

    def load_people(self, file_name):
        try:
            file = open(file_name, 'r')
        except:
            return cprint('Wrong file', "red")
        else:
            for line in file:
                item = line.split()
                if len(item) == 4:
                    self.add_person(item[0], item[1], item[2], item[3])
                elif len(item) == 3:
                    self.add_person(item[0], item[1], item[2], 'N')
                else:
                    cprint('Error', "red")
                    return "Wrong file"
            cprint('People loaded succesfully', "cyan")
            return "Successfull"

    def print_room(self, name):
        '''
        Prints a specific room with all the occupants within the room. 
        '''
        all_rooms = [room.room_name for room in self.existing_rooms]
        if name.upper() in all_rooms:
            specific_room = [room for room in self.existing_rooms if room.room_name == name.upper()]
            occupants_available = [person for person in specific_room[0].occupants]
            cprint(specific_room[0].room_name, "magenta") 
            cprint([person.first_name for person in occupants_available], "magenta")
        else:
            return cprint("Invalid room name. Room does not exist.", "red")


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
        return cprint("Data saved.", "magenta")

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
            return cprint("Wrong file", "red")

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
            return cprint("Load Successfull!!", "cyan")     


             

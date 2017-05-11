import random
import os
from termcolor import colored, cprint
from sqlalchemy import create_engine
from app.persons import Person, Fellow, Staff
from app.rooms import Room, LivingSpace, Office
from app.database import Base, Persons, Rooms
from sqlalchemy.orm import sessionmaker


class Amity(object):
    def __init__(self):
        self.existing_rooms = []
        self.every_person = []
        self.unallocated = []

    def create_room(self, room_name, room_type):
        '''
        Creates room, either living space or ofice if room name does not exist in the system.

        '''
        rooms = [room.room_name for room in self.existing_rooms]
        if room_name.upper() in rooms:
            cprint("%s already exists" %room_name, "red")
            return "%s already exists" %room_name
        if room_type.upper() == "LIVINGSPACE":
            l_space = LivingSpace(room_name.upper())
            self.existing_rooms.append(l_space)
            cprint("Living Space successfully created", "green")
            return "Living Space successfully created"
        if room_type.upper() == "OFFICE":
            office = Office(room_name.upper())
            self.existing_rooms.append(office)
            cprint("Office successfully created", "green")
            return "Office successfully created"
        if room_type.upper() not in ['OFFICE', 'LIVINGSPACE']:
            cprint("Invalid room type, should be LIVINGSPACE or OFFICE", "red")
            return "Invalid room type, should be LIVINGSPACE or OFFICE"

    def add_person(self, first_name, last_name, person_title, accomodation):
        '''
        Adds person either Staff or Fellow.
        Assigns an id to each person added. You can add more than one person with similar names.
        Automatically assigns person a room, if no room present person is added to the unallocated list.
        '''
        person_title = person_title.upper()
        full_name = first_name + " " + last_name
        if type(first_name) != str or type(last_name) != str:
            cprint("Error", "red")
            return "Invalid name. Name should be letters"
        if person_title.upper() not in ["STAFF", "FELLOW"]:
            cprint("Invalid role, should be STAFF or FELLOW", "red")
            return "Invalid role, should be STAFF or FELLOW"
        livingsp_available = [livingsp for livingsp in self.existing_rooms if livingsp.room_type == "LIVINGSPACE"
                               and livingsp.is_vacant()]

        offices_available = [ofice for ofice in self.existing_rooms if ofice.room_type == "OFFICE"
                             and ofice.is_vacant()]   
        fellow = Fellow(first_name, last_name) 
        staff = Staff(first_name, last_name) 


        if accomodation == "N" and person_title == "STAFF":
            if not offices_available:
                self.every_person.append(staff)
                self.unallocated.append(staff)

                return cprint("No room available. Person has been added to the unallocated list.", "yellow")
            else:
                 office = random.choice(offices_available)
                 self.every_person.append(staff)
                 office.occupants.append(fellow)
                 staff.allocation = office.room_name
                 return cprint("Person has been allocated an office", "green")
        elif accomodation == "Y" and person_title == "STAFF":
            return cprint("Sorry, Staff cant get accomodation.", "red")
        elif accomodation == "Y" and person_title == "FELLOW":
            if offices_available and livingsp_available:
                office = random.choice(offices_available)
                living_space = random.choice(livingsp_available)
                self.every_person.append(fellow)
                office.occupants.append(fellow)
                living_space.occupants.append(fellow)
                fellow.allocation = office.room_name
                fellow.accomodated = living_space.room_name
                return cprint("Succesfull. Person has been allocated to a living space and office", "green")
            if offices_available and not livingsp_available:
                office = random.choice(offices_available)
                office.occupants.append(fellow)
                fellow.allocation = office.room_name
                self.every_person.append(fellow)
                return cprint("Person has been allocated an office only. There are no living sopaces available.", "yellow")
            if livingsp_available and not offices_available:
                living_space = random.choice(livingsp_available)
                living_space.occupants.append(fellow)
                fellow.accomodated = living_space.room_name
                self.every_person.append(fellow)
                return cprint("Person has been allocated a living space only. There are no offices available.", "yellow")
            if not livingsp_available or offices_available:
                self.every_person.append(fellow)
                self.unallocated.append(fellow)
                return cprint("No room available. Person has been added to the unallocated list.", "yellow")
        else:
            if accomodation == "N" and person_title == "FELLOW":
                if not offices_available:
                    self.every_person.append(fellow)
                    self.unallocated.append(fellow)
                    return cprint("No offices available. Person has been added to the unallocated list.", "yellow")
                else:
                    office = random.choice(offices_available)
                    office.occupants.append(fellow)
                    fellow.allocation = office.room_name
                    self.every_person.append(fellow)
                    return cprint("Person has been allocated an office only.", "green")  

    def get_person(self, id_no):
        '''
        Gets person who have not been allocated to a room.
        '''
        person = [person for person in self.every_person if person.identifier == id_no]
        if not person:
            return cprint("Person id does not exist", "red")
        return person[0]
                
    def allocate_room(self, id_no, accomodation):
        '''
        Allocates room randomly using the id assigned to each person added to the system.
        Checks if there are rooms with available spaces before allocating rooms.
        Removes person from the unallocated list.
        '''
        livingsp_available = [livingsp for livingsp in self.existing_rooms if livingsp.room_type == "LIVINGSPACE"
                               and livingsp.is_vacant()]
        offices_available = [ofice for ofice in self.existing_rooms if ofice.room_type == "OFFICE"
                             and ofice.is_vacant()]  
        # person = [person for person in self.every_person if person.identifier == id_no]
        person = self.get_person(id_no)
        title = person.person_title

        if livingsp_available and offices_available:
            living_space = random.choice(livingsp_available)
            office = random.choice(offices_available)
            if person == "Person id does not exist":
                return cprint("Person id does not exist", "red")
            elif title.upper() == "FELLOW" and person.accomodation == "Y":
                if person.accomodated == None and person.allocated == None:
                    office.occupants.append(person)
                    living_space.occupants.append(person)
                    self.unallocated.remove(person)
                    return cprint("Person has been allocated office and living space", "green")
                elif person.accomodated == None and person.allocated != None:
                    living_space.occupants.append(person)
                    self.unallocated.remove(person)
                    return cprint("Person has been allocated a living space", "green")
                else:
                     if person.accomodated != None and person.allocated == None:
                         office.occupants.append(person)
                         self.unallocated.remove(person)
                         return cprint("Person has been allocated an office.", "green")
            elif title.upper() == "FELLOW" and person.accomodation == "N":
                office.occupants.append(person)
                self.unallocated.remove(person)
                return cprint("Person has been allocated an office.", "green")
            else:
                if title.upper() == "STAFF" and person.accomodation == "N":
                    office.occupants.append(person)
                    self.unallocated.remove(person)
                    return cprint("Person has been allocated an office.", "green")

        elif len(livingsp_available) > 0 and len(offices_available) == 0:
            living_space = random.choice(livingsp_available)
            if title.upper() == "STAFF" and person.accomodation == "N":
                cprint("Sorry, there are no offices available.", "yellow")
                return cprint("Create office room before allocating Staff.", "yellow")
            elif title.upper() == "STAFF" and person.accomodation == "Y":
                return cprint("Sorry, staff can not get accomodation.", "yellow")
            elif title.upper() == "FELLOW" and person.accomodation == "N":
                return cprint("Sorry, there are no offices available.", "yellow")
            else:
                if title.upper() == "FELLOW" and person.accomodation == "Y":
                    if person.accomodated == None and person.allocated == None:
                        living_space.occupants.append(person)
                        cprint("Fellow has been allocated a living space only", "green")
                        return cprint("Create room office then allocate person room.", "yellow")
                    elif person.accomodated == None and person.allocated != None:
                        living_space.occupants.append(person)
                        self.unallocated.remove(person)
                        return cprint("Fellow has been allocated a living space only", "green")
                    else:
                        if person.accomodated != None and person.allocated == None:
                            cprint("There are no offices available.", "yellow")
                            return cprint("Create office room first then allocate room.", "yellow")

        elif len(livingsp_available) == 0 and len(offices_available) > 0:
            office = random.choice(offices_available)
            if title.upper() == "STAFF" and person.accomodation == "N":
                office.occupants.append(person)
                self.unallocated.remove(person)
                return cprint("Person has been allocated an office", "green")
            elif title.upper() == "STAFF" and person.accomodation == "Y":
                return cprint("Sorry staff cant get accomodation", "red")
            elif title.upper() == "FELLOW" and person.accomodation == "Y":
                if person.accomodated == None and person.allocated == None:
                    office.occupants.append(person)
                    cprint("Fellow has been allocated office only", "yellow")
                    return ("Create room living space then allocate room", "yellow")
                elif person.accomodated == None and person.allocated != None:
                    cprint("Ther are no living space available.", "yellow")
                    return ("Create room living space then allocate room", "yellow")
                else:
                    if person.accomodated != None and person.allocated == None:
                        office.occupants.append(person)
                        self.unallocated.remove(person)
                        return ("Person has been allocated an office", "green")

        else:
            if len(livingsp_available) == 0 and len(offices_available) == 0:
                return cprint("Sorry. There are no living space or offices available", "red")


    def fetch_person(self, id_no):
        '''Gets you the person with all attributes attached to the person object.
           Gets the person using the Id assigned to the person'''

        person = [person for person in self.every_person if person.identifier == id_no]
        if not person:
            return "Sorry, person does not exist"
        return person[0]

    def fetch_room(self, name):
        '''Gets you the room with all the occupants present '''
        room = [room for room in self.existing_rooms if room.room_name == name.upper()]
        if not room:
            return "Sorry, room does not exist"
        return room[0]

    def reallocate_room(self, id_no, r_name):
        '''
        Rellocates a person to a new room. First it checks whether the person exists, and if the person exists in the list of occupants of a specific room.
           It then reallocates the person to a room if the person exists and is not in the list of occcupants of the room are reallocatig to
        '''

        person = self.fetch_person(id_no)
        room = self.fetch_room(r_name)

        if person == "Sorry, person does not exist":
            print ("Sorry, person does not exist")
            return cprint("Sorry, person does not exist", "red")
        if room == "Sorry, room does not exist":
            print ("Sorry, room does not exist")
            return cprint("Sorry, room does not exist", "red")
        
        title = person.person_title
        room_type = room.room_type
        
        if title.upper() == "STAFF" and room_type.upper() == "LIVINGSPACE":
            cprint ("Sorry staff can not be reallocated to living space", "red")
            return "Sorry staff can not be reallocated to living space"
        elif  title.upper() == "STAFF" and room_type.upper() == "OFFICE":
            room.occupants.append(person)
            return cprint("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name), "green")
        elif  title.upper() == "FELLOW" and room_type.upper() == "OFFICE":
            room.occupants.append(person)
            return cprint("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name), "green")
        else:
            if title.upper() == "FELLOW" and room_type.upper() == "LIVINGSPACE":
                room.occupants.append(person)
                return cprint("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name), "green")
        for room in self.existing_rooms:
            occupant_found = [ person for person in room.occupants if person.identifier == id_no]
            if len(occupant_found)>0:
                room.occupants.remove(person)
        cprint("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name), "green")
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
            output += "OFFICE:\n"

            for room in offices:
                output += room.room_name.upper() + "\n" + ("-" * 40 + "\n")
                for occupant in room.occupants:
                    output += "{}".format(occupant.full_name) + ", "

                output+="\n\n"

            living_space = [room for room in self.existing_rooms if room.room_type == "LIVINGSPACE"]
            output += "LIVING SPACE:\n"

            for room in living_space:
                output += room.room_name.upper() + "\n" + ("-" * 40 + "\n")
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
            return cprint("Succesful!! The allocations have been saved in {}".format(file_name), "green")


    def print_unallocated(self, file_name=None):
        '''
        Prints all unallocated.
        '''
        output = ''
        output += 'Identifier  ' + '\t' + 'First Name  ' + '\t' + 'Last Name  ' + '\t' + 'Role' + '\t' + 'Accomodation' + '\n'
        for person in self.unallocated:
            output += str(person.identifier) + '\t' + person.first_name  + '\t\t' + person.last_name + '\t\t' + person.person_title + '\t\t' + person.accomodation + '\n'

        cprint(output, "cyan")
        if len(self.unallocated) == 0:
            return cprint("The unallocated list is empty", "yellow")
        return cprint("Successfull", "green")    

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
            cprint('People loaded succesfully', "green")
            return "Successfull"

    def print_room(self, name):
        '''
        Prints a specific room with all the occupants within the room.
        '''
        room = [room for room in self.existing_rooms if room.room_name == name.upper()]
        if not room:
            return cprint("Invalid room name. Room does not exist.", "red")
        output = ''
        output += 'Identifier  ' + '\t' + 'First Name  ' + '\t' + 'Last Name  ' + '\t' + 'Role' + '\t' + 'Accomodation' + '\n'
        for occupant in room[0].occupants:
            output += str(occupant.identifier) + '\t' + occupant.first_name  + '\t\t' + occupant.last_name + '\t\t' + occupant.person_title + '\t\t' + occupant.accomodation + '\n'

        cprint(output, "cyan")

    def save_state(self, file_name=None):
        '''
        Saves all data input to the data base 
        '''

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
            occupants_names = ",".join(str_occupants)

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
        return cprint("Data saved.", "cyan")
    def print_persons(self, file_name=None):
        '''
        Prints every person that has been added to the system.
        '''
        output = ''
        output += 'Identifier  ' + '\t' + 'First Name  ' + '\t' + 'Last Name  ' + '\t' + 'Role' + '\t' + 'Accomodation' + '\n'
        for person in self.every_person:
            output += str(person.identifier) + '\t' + person.first_name  + '\t\t' + person.last_name + '\t\t' + person.person_title + '\t\t' + person.accomodation + '\n'

        cprint(output, "cyan")
        if len(self.every_person) == 0:
            return cprint("No persons added to the system.", "yellow")
        return cprint("Successfull", "green")

    def delete_person(self, id_no):
        '''
        Deletes person from system.
        Deletes person from room occupants.
        Deletes person frm unalloated list.  
        '''
        person = [person for person in self.every_person if person.identifier == id_no]
        unallocated_person = [person for person in self.unallocated if person.identifier == id_no] 
       
        if not person:
             return cprint("Invalid ID", "yellow")

        self.every_person.remove(person[0])

        for room in self.existing_rooms:
            for occupant in room.occupants:
                if person[0].identifier == occupant.identifier:
                    room.occupants.remove(person[0])
                    return cprint("Person has been deleted", "green")            

        if unallocated_person:
            self.unallocated.remove(unallocated_person[0])
            return cprint("Person has been deleted", "green")

    def delete_room(self, room_name):
        '''
        Deletes room from the system.
        '''
        if not self.existing_rooms:
            return cprint("No rooms available", "yellow") 
        room = [room for room in self.existing_rooms if room.room_name.upper() == room_name.upper()]
        if not room:
            return cprint("The room name does not exist", "yellow")

        self.existing_rooms.remove(room[0])
        return cprint("Room has been deleted.", "green")

    def load_state(self, file_name=None):
        '''
        Loads system with data from the data base
        '''
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
                    occupant_names = room.occupants.split(",")
                    for name in occupant_names:
                        the_person = [person for person in self.every_person if person.full_name == name]
                        if len(the_person) != 0:
                            office.occupants.append(the_person[0])

                self.existing_rooms.append(office)
            else:
                living_space = LivingSpace(room.room_name)
                if len(room.occupants) == 0:
                    occupant_names = room.occupants.split(",")
                    for name in occupant_names:
                        the_person = [person for person in self.every_person if person.full_name == name]
                        if len(the_person) != 0:
                            living_space.occupants.append(the_person[0])

                self.existing_rooms.append(living_space)
            return cprint("Load Successfull!!", "green")

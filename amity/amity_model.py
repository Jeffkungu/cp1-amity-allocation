import random
import os
from termcolor import colored, cprint
from sqlalchemy import create_engine
from amity.persons import Person, Fellow, Staff
from amity.rooms import Room, LivingSpace, Office
from amity.database import Base, Persons, Rooms
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
        fellow = Fellow(first_name, last_name)

        if len(livingsp_available) > 0 and len(offices_available) > 0:
            living_space = random.choice(livingsp_available)
            office = random.choice(offices_available)
            if person == "Person id does not exist":
                return cprint("Person id does not exist", "red")
            elif title.upper() == "FELLOW" and person.accomodation == "Y":
                if fellow.accomodated == None and fellow.allocated == None:
                    office.occupants.append(person)
                    living_space.occupants.append(person)
                    self.unallocated.remove(person)
                    return cprint("Person has been allocated office and living space", "green")
                elif fellow.accomodated == None and fellow.allocated != None:
                    living_space.occupants.append(person)
                    self.unallocated.remove(person)
                    return cprint("Person has been allocated a living space", "green")
                else:
                     if fellow.accomodated != None and fellow.allocated == None:
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
                cprint("Creqate office room before allocating Staff.", "yellow")
            elif title.upper() == "STAFF" and person.accomodation == "Y":
                cprint("Sorry, staff can not get accomodation.", "yellow")
            elif title.upper() == "FELLOW" and person.accomodation == "N":
                cprint ("Sorry, there are no offices available.", "yellow")
            else:
                if title.upper() == "FELLOW" and person.accomodation == "Y":
                    if fellow.accomodated == None and fellow.allocated == None:
                        living_space.occupants.append(person)
                        
                         
                    
            

                  
                #elif title.upper() == "FELLOW" and person.accomodation == "Y":   

            

        #     if person[0].person_title.upper() == "STAFF":
        #         if accomodation == "Y":
        #             office.occupants.append(person[0])
        #             person[0].allocation = office.room_name
        #             cprint("%s has been allocated an office only"% person[0].first_name, "green")
        #             return "Staff can not get accomodation"
        #         elif accomodation == "N":
        #             office.occupants.append(person[0])
        #             person[0].allocation = office.room_name
        #             cprint("%s has been allocated an office."% person[0].first_name, "green")
        #             return "Successfull person has been allocated an office."
        #         else:
        #             cprint("Error", "red")
        #             return "Invalid input, choice of accomodation should be Y or N"
        #     elif person[0].person_title.upper() == "FELLOW":
        #         if accomodation == "Y":
        #            office.occupants.append(person[0])
        #            living_space.occupants.append(person[0])
        #            person[0].accomodated = living_space.room_name
        #            person[0].allocation = office.room_name
        #            cprint("%s has been allocated an office and a living space."% person[0].first_name, "green")
        #            return "Successfull person has been allocated office and living space"
        #         elif accomodation == "N":
        #             office.occupants.append(person[0])
        #             person[0].allocation = office.room_name
        #             cprint("%s has been allocated an office."% person[0].first_name, "green")
        #             return "Successfull person has been allocated an office only."
        #         else:
        #             cprint("Error", "red")
        #             return "Invalid input, choice of accomodation should be Y or N"
        #     else:
        #         return cprint("Invalid input, person title should be FELLOW or STAFF", "red")

        # elif len(livingsp_available) == 0 and len(offices_available) > 0:
        #      office = random.choice(list(offices_available))
        #      if person[0].person_title.upper() == "STAFF":
        #          if accomodation == "Y":
        #              office.occupants.append(person[0])
        #              person[0].allocation = office.room_name
        #              cprint("%s has been allocated an office only"% person[0].first_name, "green")
        #              return "Staff can not get accomodation"
        #          elif accomodation == "N":
        #               office.occupants.append(person[0])
        #               person[0].allocation = office.room_name
        #               cprint("%s has been allocated an office."% person[0].first_name, "green")
        #               return "Successfull person has been allocated an office."
        #          else:
        #              cprint("Error", "red")
        #              return "Invalid input, choice of accomodation should be Y or N"
        #      elif person[0].person_title.upper() == "FELLOW":
        #          if accomodation == "Y":
        #                office.occupants.append(person[0])
        #                person[0].allocation = office.room_name
        #                return cprint("%s has been allocated an office only, there are no living spaces available"% person[0].first_name, "green")
        #          elif accomodation == "N":
        #               office.occupants.append(person[0])
        #               person[0].allocation = office.room_name
        #               cprint("%s has been allocated an office."% person[0].first_name, "green")
        #               return "Successfull person has been allocated an office only."
        #          else:
        #              cprint("Error", "red")
        #              return "Invalid input, choice of accomodation should be Y or N"
        #      else:
        #          cprint("Error", "red")
        #          return "Invalid input, person title should be FELLOW or STAFF"

        # elif len(livingsp_available) > 0 and len(offices_available) == 0:
        #     living_space.occupants.append(person[0])
        #     if person[0].person_title.upper() == "STAFF":
        #          if accomodation == "Y":
        #              cprint("Failed.", "red")
        #              return "Staff can not get accomodation"
        #          elif accomodation == "N":
        #              return cprint("Sorry. There are no offices available", "red")
        #          else:
        #              cprint("Error", "red")
        #              return "Invalid input, choice of accomodation should be Y or N"
        #     elif person[0].person_title.upper() == "FELLOW":
        #         if accomodation == "Y":
        #             living_space.occupants.append(person[0])
        #             person[0].living_space = living_space.room_name
        #             return cprint("Successful. %s has been allocated living space only. \nThere are no offices available"% person[0].first_name, "green")
        #         elif accomodation == "N":
        #             return cprint("Sorry. There are no offices available", "red")
        #         else:
        #             return cprint("Invalid input. Choice of accomodation should be Y or N", "red")
        #     else:
        #         return cprint("Invalid input, person title should be FELLOW or STAFF", "red")

        # else:
        #     if len(livingsp_available) == 0 and len(offices_available) == 0:
        #         return cprint("Sorry. There are no living space or offices available", "red")

    def fetch_person(self, id_no):
        '''Gets you the person with all attributes attached to the person object.
           Gets the person using the Id assigned to the person'''

        person = [person for person in self.every_person if person.identifier == id_no]
        if not person:
            return "Sorry, person does not exist"
        return person[0]

    def fetch_room(self, name):
        '''Gets you the room with all the occupants present '''
        room = [room for room in self.existing_rooms if room.room_name == name]
        if not room:
            return "Sorry, room does not exist"
        return  room[0]

    def reallocate_room(self, id_no, r_name):
        '''
        Rellocates a person to a new room. First it checks whether the person exists, and if the person exists in the list of occupants of a specific room.
           It then reallocates the person to a room if the person exists and is not in the list of occcupants of the room are reallocatig to
        '''

        person = self.fetch_person(id_no)
        title = person.person_title
        room = self.fetch_room(r_name)
        r_type = room.room_type

        if person == "Sorry, person does not exist":
            print ("Sorry, person does not exist")
            return cprint("Sorry, person does not exist", "red")
        if room == "Sorry, room does not exist":
            print ("Sorry, room does not exist")
            return cprint("Sorry, room does not exist", "red")
        else:
            if title.upper() == "STAFF" and r_type.upper() == "LIVINGSPACE":
                cprint ("Sorry staff can not be reallocated to living space", "red")
                return "Sorry staff can not be reallocated to living space"
            elif  title.upper() == "STAFF" and r_type.upper() == "OFFICE":
                room.occupants.append(person)
                return cprint("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name), "green")
            elif  title.upper() == "FELLOW" and r_type.upper() == "OFFICE":
                room.occupants.append(person)
                return cprint("{} has been successfully reallocated to {} ".format(person.first_name, room.room_name), "green")
            else:
                if title.upper() == "FELLOW" and r_type.upper() == "LIVINGSPACE":
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
            return cprint("Succesful!! The allocations have been saved in {}".format(file_name), "green")


    def print_unallocated(self, file_name=None):
        '''
        Prints all unallocated.
        '''
        output = ''
        output += 'Identifier  ' + '\t' + 'First Name  ' + '\t' + 'Last Name  ' + '\t' + 'Type' + '\n'
        for person in self.unallocated:
            output += str(person.identifier) + '\t' + person.first_name  + '\t\t' + person.last_name + '\t\t' + person.person_title + '\n'

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
        all_rooms = [room.room_name for room in self.existing_rooms]
        if name.upper() in all_rooms:
            specific_room = [room for room in self.existing_rooms if room.room_name == name.upper()]
            occupants_available = [person for person in specific_room[0].occupants]
            cprint(specific_room[0].room_name, "cyan")
            cprint([person.first_name for person in occupants_available], "cyan")
            return "Successfull"
        else:
            return cprint("Invalid room name. Room does not exist.", "red")


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

import random
import os
from termcolor import colored
from person.persons import Person, Fellow, Staff
from room.rooms import Room, LivingSpace, Office

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
            return "Invalid name, should be letters"
        else:
            if person_title.upper() not in ["STAFF", "FELLOW"]:
                return "Invalid title, should be STAFF or FELLOW"
            elif accomodation == "N" and person_title == "FELLOW" or "STAFF":
                self.every_person.append(Fellow(first_name, last_name))
                self.every_person.append(Staff(first_name, last_name))
                return ("%s successfully added"% full_name)
            elif accomodation == "Y" and person_title == "FELLOW":
                 self.every_person.append(Fellow(first_name, last_name))
                 return ("%s successfully added"% full_name)
            else:
                if accomodation == "Y" and person_title == "STAFF":
                    return "Invalid input, staff can not get accomodation"

    def allocate_room(self, first_name, last_name, person_title, accomodation):
        livingsp_available = [l for l in self.existing_rooms if l.room_type == "LIVING SPACE"
                               and l.max_capacity > len(l.occupants)]
        offices_available = [o for o in self.existing_rooms if o.room_type == "OFFICE"
                             and o.max_capacity > len(o.occupants)]
        full_name = first_name + " " + last_name 

        if len(livingsp_available) > 0 and len(offices_available) > 0:
            living_space = random.choice(list(livingsp_available))
            office = random.choice(list(offices_available))
            if person_title.upper() == "STAFF":
                if accomodation == "Y":
                    office.occupants.append(full_name)
                    return ("%s has been allocated an office only, staff can not get accomodation"% full_name)
                elif accomodation == "N":
                    office.occupants.append(full_name)
                    return ("Successfull %s has been allocated an office."% full_name)
                else:
                    return "Invalid input, choice of accomodation should be Y or N"
            elif person_title.upper() == "FELLOW":
                if accomodation == "Y":
                   office.occupants.append(full_name)
                   living_space.occupants.append(full_name)
                   return ("Successfull %s has been allocated an office and a living space."% full_name)
                elif accomodation == "N":
                    office.occupants.append(full_name)
                    return ("Successfull %s has been allocated an office."% full_name)
                else:
                    return "Invalid input, choice of accomodation should be Y or N"
            else:
                return "Invalid input, person title should be FELLOW or STAFF"        

        elif len(livingsp_available) == 0 and len(offices_available) > 0:
             office = random.choice(list(offices_available))
             if person_title.upper() == "STAFF":
                 if accomodation == "Y":
                     office.occupants.append(full_name)
                     return ("%s has been allocated an office only, staff can not get accomodation"% full_name)
                 elif accomodation == "N":
                      office.occupants.append(full_name)
                      return ("Successfull %s has been allocated an office."% full_name)
                 else:
                     return "Invalid input, choice of accomodation should be Y or N"
             elif person_title.upper() == "FELLOW":
                 if accomodation == "Y":
                       office.occupants.append(full_name)
                       return ("%s has been allocated an office only, there are no living spaces available"% full_name)
                 elif accomodation == "N":
                      office.occupants.append(full_name)
                      return ("Successful.%s has been allocated an office."% full_name)
                 else:
                     return "Invalid input, choice of accomodation should be Y or N"
             else:
                 return "Invalid input, person title should be FELLOW or STAFF"
         
        elif len(livingsp_available) > 0 and len(offices_available) == 0:
            living_space.occupants.append(full_name)
            if person_title.upper() == "STAFF":
                 if accomodation == "Y":
                     return "Failed, staffs can not get accomodation"
                 elif accomodation == "N":
                     return "Sorry. There are no offices available"
                 else:
                     return "Invalid input. Choice of accomodation should be Y or N"
            elif person_title.upper() == "FELLOW":
                if accomodation == "Y":
                    living_space.occupants.append(full_name)
                    return ("Successful. %s has been allocated living space only. \nThere are no offices available"%full_name)
                elif accomodation == "N":
                    return "Sorry. There are no offices available"
                else:
                    return "Invalid input. Choice of accomodation should be Y or N"
            else:
                return "Invalid input, person title should be FELLOW or STAFF"

        else:
            if len(livingsp_available) == 0 and len(offices_available) == 0:
                return "Sorry. There are no living space or offices available"

    def fetch_person(self, identifier):
        '''Gets you the person with all attributes attached to the person object.
           Gets the person using the Id assigned to the person'''
        identifiers = [person.identifier for person in self.every_person]
        person = None  
        if identifier in identifiers:
            if identifier == person.identifier:
                person = person.identifier
                return person
            else:
                return "Sorry, Id does not match any person"
        else:
            return "Sorry, person does not exist"

    def fetch_room(self, room_name):
        '''Gets you the room with all the occupants present '''
        rooms = [room.room_name for room in self.existing_rooms]
        room_object = None
        if room_name in rooms:
            if room_name == room.room_name:
                room_object = room.room_name
                return room_object
            else:
                return "Sorry, room name does not match any rooms"
        else:
            return "Sorry, room does not exist"                
        
    def reallocate_room(self, first_name,last_name, room_name):
        '''Rellocates a person to a new room. First it checks whether the person exists, and if the person exists in the list of occupants of a specific room.
           It then reallocates the person to a room if the person exists and is not in the list of occcupants of the room are reallocatig to'''
        person = self.fetch_person(identifier)
        if person == "Sorry, Id does not match any person":
            print ('Check the Id, it does not match any person')
            return "Check the Id, it does not match any person"
        elif person == "Sorry, person does not exist":
            print ("Sorry, person does not exist")
            return "Sorry, person does not exist"

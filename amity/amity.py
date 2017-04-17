import random
import os
from person.persons import Person, Fellow, Staff
from room.rooms import Room, LivingSpace, Office

class Amity(object):
    def __init__(self):
        self.existing_rooms = []
        self.every_person = []
        self.first_name = first_name
        self.last_name = last_name


    def create_room(self, room_name, room_type):
        r = [x.room_name for x in self.existing_rooms]
        if room_name.upper() in r:
            return 'Room already exists'
        else:
            if room_type.upper() == "LIVING SPACE":
                self.existing_rooms.append(LivingSpace(room_name.upper()))
                return "Living Space successfully created"
            elif room_type.upper() == "OFFICE":
                  self.existing_rooms.append(Office(room_name.upper()))
                  return "Office successfully created"
            else:
                return "Invalid room type, should be LIVING SPACE or OFFICE"

    def add_person(self, first_name, last_name, person_title, accomodation):
        full_name = self.first_name + " " + self.last_name
        p = [x.full_name for x in self.every_person]
        if person_title.upper() == "STAFF":
            if full_name in p:
                return "Person already exists"
            else:
                self.every_person.append(Staff(full_name))
                return "Person successfully added"
        elif person_title.upper() == "FELLOW":
            if full_name in p:
                return "Person already exists"
            else:
                self.every_person.append(Fellow(full_name))
                return "Person successfully added"
                                
            
class Room(object):
    def __init__(self, room_name, room_type, max_capacity):
        self.room_name = room_name
        self.room_type = room_type
        self.max_capacity = max_capacity
        self.occupants = []

class Office(Room):
    def __init__(self, room_name):
        super(Office, self).__init__(room_name=room_name, room_type = "OFFICE", max_capacity = 6, )
        self.occupants = []

    def is_vacant(self):
        return len(self.occupants) !=  self.max_capacity    

class LivingSpace(Room):
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name=room_name, room_type = "LIVINGSPACE", max_capacity = 4)
        self.occupants = []

    def is_vacant(self):
        return len(self.occupants) !=  self.max_capacity  
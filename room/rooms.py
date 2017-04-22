class Room(object):
    def __init__(self, room_name, room_type, max_capacity):
        self.room_name = room_name
        self.room_type = room_type
        self.max_capacity = max_capacity
        self.occupants = []

class Office(Room):
    def __init__(self, room_name):
        super(Office, self).__init__(room_name=room_name, room_type = "OFFICE", max_capacity = 6, )

class LivingSpace(Room):
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name=room_name, room_type = "LIVING SPACE", max_capacity = 4)
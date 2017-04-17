class Room(object):
    def __init__(self, room_name, room_type, max_capacity):
        self.room_name = room_name
        self.room_type = room_type
        self.max_capacity = max_capacity

class Office(Room):
    def __init__(self):
        super(Office, self).__init__(room_type="OFFICE", max_capacity=6)

class LivingSpace(Room):
    def __init__(self):
        super(LivingSpace, self).__init__(room_type="LIVING SPACE", max_capacity=4)                   
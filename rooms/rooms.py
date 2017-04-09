class Room(object):
    def __init__(self, room_name, room_title, max_capacity):
        self.room_name = room_name
        self.room_title = room_title
        self.max_capacity = max_capacity

class Office(Room):
    def __init__(self):
        super(Office, self).__init__(room_title="Office", max_capacity=6)

class LivingSpace(Room):
    def __init__(self):
        super(LivingSpace, self).__init__(room_title="Livingspace", max_capacity=4)                   
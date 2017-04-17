import unittest
from rooms.rooms import Room, Office, LivingSpace

class TestRoomsModule(unittest.TestCase):
    def Test_Office_room_title(self):
        o = Office()
        self.assertEqual(o.room_title, "Office")

    def Test_Office_max_caacity(self):
        o = Office()
        self.assertEqual(o.max_capacity, 6)

    def Test_Living_space_room_title(self):
        l = LivingSpace()
        self.assertEqual(l.room_title, "Livingspace")

    def Test_Living_space_max_capacity(self):
        l = LivingSpace()
        self.assertEqual(l.max_capacity, 4)    
                

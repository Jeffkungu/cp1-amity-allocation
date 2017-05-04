import unittest
from amity.rooms import Room, Office, LivingSpace

class TestRoomsModule(unittest.TestCase):
    def Test_Office_room_title(self):
        office = Office("VALHALLA")
        self.assertEqual(office.room_type, "OFFICE")

    def Test_Office_max_caacity(self):
        office = Office("VALHALLA")
        self.assertEqual(office.max_capacity, 6)

    def Test_Living_space_room_title(self):
        livingspace = LivingSpace("PHP")
        self.assertEqual(livingspace.room_type, "LIVING SPACE")

    def Test_Living_space_max_capacity(self):
        livingspace = LivingSpace("PHP")
        self.assertEqual(livingspace.max_capacity, 4)    
                

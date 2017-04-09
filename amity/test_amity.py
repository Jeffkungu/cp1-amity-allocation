import unittest


class TestAmityModule(unittest.TestCase):
    def setUp(self):
        pass

    def Test_load_sytem(self):
        self.assertEqual(self.amity.load_system(), 'System successfully Loaded', msg='Loading Failed') 

    def Test_create_room(self):
        self.assertEqual(self.amity.create_room('Valhalla', 'Office'), 'Room successfully created', msg="Room not created")

    def Test_check_if_room_exists(self):
        self.amity.create_room('Valhalla', 'Office')
        self.assertEqual(self.amity.create_room('London', 'OFFICE'), 'Room already exists', msg="Room doesn't exist")

    def Test_for_wrong_room_type_created(self):
        self.assertEqual(self.amity.create_room('Valhlla', 'Random'), 'Room type entered does not exist. Please insert Office or Living space')

    def Test_add_person(self):
        self.assertEqual(self.amity.add_person('Jeff', 'Kungu', 'Fellow', 'Y'), 'Person Succesfully Added', msg="Failed. Person was not added")

    def Test_check_if_person_exists(self):
        self.amity.add_person('Jeff', 'Kungu', 'Fellow', 'Y')
        self.assertEqual(self.amity.add_person('Jeff', 'Kungu', 'Fellow', 'Y'), 'Person already exists')

    def Test_allocate_living_space_to_fellow(self):
        self.assertEqual(self.amity.allocate_room('Jeff Kungu', 'Fellow', 'Y'), 'Living Space successfully allocated')

    def Test_allocate_office_to_fellow(self):
        self.assertEqual(self.amity.allocate_room('Jeff Kungu', 'Fellow', 'Y'), 'Office successfully allocated')

    def Test_allocate_office_to_staff(self):
        self.assertEqual(self.amity.allocate_room('John Doe', 'Staff', 'N'), 'Living Space successfully allocated')

    def Test_allocate_livin_space_to_staff(self):
        self.assertEqual(self.amity.allocate_room('John Doe', 'Staff', 'N'), 'Failed. Staff can not have any accomodation)                







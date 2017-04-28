import unittest
from amity.amity_model import Amity



class TestAmityModule(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def Test_create_existing_room(self):
        self.amity.create_room("Ruby", "Office")
        self.assertEqual(self.amity.create_room("Ruby", "Office"),
                         'Room Ruby already exists')

    def Test_create_Livinspace(self):
        self.assertEqual(self.amity.create_room('PYTHON', 'LIVING SPACE'), 'Living Space successfully created')

    def Test_create_Office(self):
        self.assertEqual(self.amity.create_room('Krypton', 'OFFICE'), 'Office successfully created')

    def Test_for_invalid_room_type_created(self):
        self.assertEqual(self.amity.create_room('Valhalla', 'Random'), "Invalid room type, should be LIVING SPACE or OFFICE")

    def Test_add_person_interger_name(self):
        self.assertEqual(self.amity.add_person(123, 123, 'Fellow', 'Y'), "Invalid name. Name should be letters")

    def Test_add_person_invalid_role(self):
        self.assertEqual(self.amity.add_person('Jeff', 'Kungu', 'Random', 'Y'), "Invalid role, should be STAFF or FELLOW")

    def Test_add_fellow_without_accomodation(self):
        self.assertEqual(self.amity.add_person('Jeff', 'Kungu', 'Fellow', 'N'), "Jeff Kungu successfully added", id(self))

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
        self.assertEqual(self.amity.allocate_room('John Doe', 'Staff', 'N'), 'Failed. Staff can not have any accomodation')
    
    def Test_load_state(self):
        self.assertEqual(self.amity.load_state(), 'System successfully Loaded', msg='Loading Failed') 

if __name__ == '__main__':
    unittest.main()

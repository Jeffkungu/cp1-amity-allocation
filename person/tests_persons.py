import unittest
from person.persons import Person, Fellow, Staff

class TestPersonsModule(unittest.TestCase):
    def Test_Fellow_title(self):
        f = Fellow("Jeff", "Kungu")
        self.assertEqual(f.person_title, "Fellow")

    def Test_if_Fellow_wants_accomodation(self):
        f = Fellow("Jeff", "Kungu")
        self.assertEqual(f.accomodation, "Y")

    def Test_Staff_title(self):
        s = Staff("John", "Doe")
        self.assertEqual(s.person_title, "Staff")

    def Test_if_Staff_wants_accomodation(self):
        s = Staff("John", "Doe")
        self.assertEqual(s.accomodation, "N")            
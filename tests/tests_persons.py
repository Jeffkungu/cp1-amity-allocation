import unittest
from amity.persons import Person, Fellow, Staff

class TestPersonsModule(unittest.TestCase):
    def Test_Fellow_title(self):
        fellow = Fellow("Jeff", "Kungu")
        self.assertEqual(fellow.person_title, "FELLOW")

    def Test_if_Fellow_wants_accomodation(self):
        fellow = Fellow("Jeff", "Kungu")
        self.assertEqual(fellow.accomodation, "Y")

    def Test_Staff_title(self):
        staff = Staff("John", "Doe")
        self.assertEqual(staff.person_title, "STAFF")

    def Test_if_Staff_wants_accomodation(self):
        staff = Staff("John", "Doe")
        self.assertEqual(staff.accomodation, "N")            
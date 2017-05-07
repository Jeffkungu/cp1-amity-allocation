import unittest
from amity.amity_model import Amity
from amity.rooms import Room, LivingSpace, Office
from amity.persons import Person, Fellow, Staff
from amity.database import Base, Persons, Rooms, Allocations
from sqlalchemy.orm import sessionmaker


class TestAmityModule(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def test_create_existing_room(self):
        '''
        Tests the return value after adding a room that already exists
        '''
        self.amity.create_room("Ruby", "Office")
        self.assertEqual(self.amity.create_room("Ruby", "Office"), 'Ruby already exists')

    def test_create_Livinspace(self):
        '''
        Tests the return value after adding a living space that was not there before
        '''
        self.assertEqual(self.amity.create_room('PYTHON', 'LIVINGSPACE'), 'Living Space successfully created')

    def test_create_Office(self):
        '''
        Tests the return value after adding an office that was not there before
        '''
        self.assertEqual(self.amity.create_room('Krypton', 'OFFICE'), 'Office successfully created')

    def test_invalid_room_type_created(self):
        '''
        Tests return message after inputing the wrong room type when creating a new room
        '''
        self.assertEqual(self.amity.create_room('Valhalla', ' '), "Invalid room type, should be LIVING SPACE or OFFICE")

    # def test_add_person_interger_name(self):
    #     self.assertEqual(self.amity.add_person(123, 234, 'FELLOW', 'Y'), "Invalid name. Name should be letters")

    def test_add_person_invalid_role(self):
        '''
        Tests return value when adding a person with the wrong input as person title
        '''
        self.assertEqual(self.amity.add_person('Jeff', 'Kungu', 'RANDOM', 'Y'), "Invalid role, should be STAFF or FELLOW")

    def test_add_fellow_without_accomodation(self):
        '''
        Tests the return value when you add a person who is a felllow and does not want accomodqtaion
        '''
        self.assertEqual(self.amity.add_person('Jeff', 'Kungu', 'FELLOW', 'N'), "Person successfully added")

    def test_add_staff_accomodation_is_Y(self):
        '''
        Tests the return value when you add a person who is a staff wants accomodqtaion
        '''
        self.assertEqual(self.amity.add_person("Tony", "Kungu", "STAFF", "Y"),  "Invalid input, staff can not get accomodation")

    def test_allocate_room_staff_wants_accomodation(self):
        '''
        Test return value when allocating a room to staff with accomodation option as Y
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.create_room("Valhalla", "LIVING SPACE")
        # add person
        self.amity.add_person('Teddy', "Kungu", "STAFF", "N")
        # get object of added persion
        person_object = self.amity.every_person[0]
        self.assertEqual(self.amity.allocate_room(person_object.identifier,'Y'), "Staff can not get accomodation")

    def test_allocate_room_staff_no_accomodation(self):
        '''
        Test return value when allocating room randomly to staff with accomodation option as N
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.create_room("Valhalla", "LIVING SPACE")
        # add person
        self.amity.add_person('Teddy', "Kungu", "STAFF", "N")
        # get object of added persion
        person_object = self.amity.every_person[0]
        self.assertEqual(self.amity.allocate_room(person_object.identifier,'N'), "Successfull person has been allocated an office.")

    def test_allocate_room_fellow_no_accomodation(self):
        '''
        Test return value when allocating room randomly to fellow with accomodation option as N
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.create_room("Valhalla", "LIVING SPACE")
        # add person
        self.amity.add_person('Teddy', "Kungu", "FELLOW", "N")
        # get object of added persion
        person_object = self.amity.every_person[0]
        self.assertEqual(self.amity.allocate_room(person_object.identifier, 'N'), "Successfull person has been allocated an office only.")

    def test_allocate_room_fellow_wants_accomodation(self):
        '''
        Test return value when allocating room randomly to fellow with accomodation option as Y
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.create_room("Valhalla", "LIVINGSPACE")
        # add person
        self.amity.add_person('Teddy', "Kungu", "FELLOW", "Y")
        # get object of added persion
        person_object = self.amity.every_person[0]
        self.assertEqual(self.amity.allocate_room(person_object.identifier, 'Y'), "Successfull person has been allocated office and living space")

    def test_allocate_room_staff_wrong_acccomodation_input(self):
        '''
        Test return value when allocating room randomly to staff with accomodation option not N or Y
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.create_room("Valhalla", "LIVING SPACE")
        self.amity.add_person('Teddy', "Kungu", "STAFF", "N")
        person_object = self.amity.every_person[0]
        self.assertEqual(self.amity.allocate_room(person_object.identifier,'Random'), "Invalid input, choice of accomodation should be Y or N")

    def test_allocate_room_fellow_wrong_acccomodation_input(self):
        '''
        Test return value when allocating room randomly to fellow with accomodation option not N or Y
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.create_room("Valhalla", "LIVINGSPACE")
        self.amity.add_person('Teddy', "Kungu", "FELLOW", "Y")
        person_object = self.amity.every_person[0]
        self.assertEqual(self.amity.allocate_room(person_object.identifier,'Random'), "Invalid input, choice of accomodation should be Y or N")


    def test_fetch_person_wrong_id(self):
        '''
        Test return value when you fetch person who does not exist in the system
        '''
        self.amity.add_person("Jeff", "Kungu", "FELLOW", "Y")
        self.assertEqual(self.amity.fetch_person("Random"), "Sorry, person does not exist")

    def test_fetch_room_not_existing(self):
        '''
        Test return value when you fetch room which does not exist in the system
        '''        
        self.amity.create_room("PYTHON", "LIVING SPACE")
        self.amity.create_room("KRYPTON", "OFFICE")
        self.assertEqual(self.amity.fetch_room("Random"), "Sorry, room does not exist")

    def test_reallocate_room_successfull(self):
        '''
        Test return value when you reallocate person to a new room
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.add_person('Teddy', "Kungu", "FELLOW", "Y")
        person_object = self.amity.every_person[0]
        self.amity.allocate_room(person_object.identifier,'Y')
        self.amity.create_room("PYTHON", "OFFICE")
        self.assertEqual(self.amity.reallocate_room(person_object.identifier, "PYTHON"), "Successful")

    def test_load_people(self):
        '''
        Test return value when you succesfully load people from an exiting txt file into the system
        '''
        file = open("people.txt", "w")
        persons = ["OLUWAFEMI, " "SULE, " "FELLOW, " "Y"]
        file.writelines(persons)
        file.close()
        self.assertEqual(self.amity.load_people("people.txt"), "Successfull")

    def test_print_unallocated(self):
        '''
        Test the return value when you print the unallocated 
        '''
        self.amity.add_person('Teddy', "Kungu", "FELLOW", "Y")
        self.assertEqual(self.amity.print_unallocated(), "Successfull")

    def test_print_room(self):
        '''
        Test the return value when you print an existing room
        '''
        self.amity.create_room("PHP", "OFFICE")
        self.amity.create_room("Valhalla", "LIVINGSPACE")
        self.amity.add_person('Teddy', "Kungu", "FELLOW", "Y")
        person_object = self.amity.every_person[0]
        self.amity.allocate_room(person_object.identifier,'Y')
        self.assertEqual(self.amity.print_room("PHP"), "Successfull")


if __name__ == '__main__':
    unittest.main()

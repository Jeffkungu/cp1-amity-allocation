class Person(object):
    def __init__(self, first_name, last_name, person_title, accomodation):
        self.identifier = id(self)
        self.first_name = first_name
        self.last_name = last_name
        self.person_title = person_title
        self.accomodation = accomodation
        self.full_name =  self.first_name + " " + self.last_name
        self.allocation = None
        self.accomodated = None


class Fellow(Person):
    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name=first_name, last_name=last_name, person_title="FELLOW", accomodation="Y")
        full_name = self.first_name + " " + self.last_name
        self.allocation = None
        self.accomodated = None

class Staff(Person):
    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name=first_name, last_name=last_name, person_title="STAFF", accomodation="N")
        full_name = self.first_name + " " + self.last_name
        self.allocation = None       

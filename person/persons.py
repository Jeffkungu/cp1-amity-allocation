class Person(object):
    def __init__(self, first_name, last_name, person_title, accomodation):
        self.first_name = first_name
        self.last_name = last_name
        self.person_title = person_title
        self.accomodation = accomodation
       

    def person_full_name(self):
        full_name =  self.first_name + " " + self.last_name
        self.full_name = full_name 

class Fellow(Person):
    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name=first_name, last_name=last_name, person_title="Fellow", accomodation="Y")
        full_name = self.first_name + " " + self.last_name

class Staff(Person):
    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name=first_name, last_name=last_name, person_title="Staff", accomodation="N")        

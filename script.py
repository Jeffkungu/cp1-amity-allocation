from amity.amity_model import Amity
a = Amity()
print(a.create_room("Vigor","Office"))
print(a.create_room("Juice","Living space"))
print(a.add_person("Joshua","Mwaniki","Staff","N"))
print(a.add_person("James","Bonoko","Fellow","Y"))
print(a.save_state())
from amity.amity_model import Amity
a = Amity()
print(a.add_person("Joshua","Mwaniki","Staff","N"))
identifier = [person.identifier for person in a.every_person]
print(a.create_room("Vigor","Office"))
print(a.create_room("Juice","Living space"))
print(a.add_person("Joshua","Mwaniki","Staff","N"))
print(a.add_person("James","Bonoko","Fellow","Y"))
print(a.allocate_room(identifier[0], "N"))
allocation = [person.allocation for person in a.every_person]
print (allocation)
print(a.save_state("this"))
print(a.print_unallocated())
# print(a.load_state("this"))
# print(a.print_unallocated())
# print(a.print_allocations())


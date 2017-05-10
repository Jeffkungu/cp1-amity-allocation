"""
AMITY.
Usage:
    amity create_room <room_type> <room_names>...
    amity add_person <first_name> <last_name> <person_title> ( FELLOW | STAFF ) [<accomodation>]
    amity allocate_room <id_no> <accomodation>
    amity fetch_person <id_no>
    amity fetch_room <name>
    amity reallocate_room <id_no> <r_name>
    amity print_allocations [<file_name.txt>]
    amity load_people [<file_name.txt>]
    amity print_unallocated [<file_name.txt>]
    amity print_room <name>
    amity print_persons [<file_name.txt>]
    amity delete_person <id_no>
    amity delete_room <room_names>...
    amity save_state [<file_name.db>]
    amity load_state [<file_name.db>]
    amity (-i | --interactive)
    amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
import re
from termcolor import cprint, colored
from pyfiglet import Figlet, figlet_format
from docopt import docopt, DocoptExit
from app.amity_model import Amity


def docopt_cmd(func):
    

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return
        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return
        return func(self, opt)
    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive(cmd.Cmd):

    amity = Amity()
    cprint(figlet_format("AMITY", font="rev"), "magenta", attrs=['bold'])
    #prompt = '(amity)'
    file = None
    print(__doc__)


    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_names>..."""
        room_type = arg['<room_type>']
        room_names = arg['<room_names>']
        for room_name in room_names:
            self.amity.create_room(room_name, room_type)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_title> [<accomodation>]"""

        fname = arg["<first_name>"].upper()
        lname = arg["<last_name>"].upper()
        role = arg["<person_title>"].upper()
        wants_accommodation = arg["<accomodation>"].upper()
        if re.match("^[a-zA-Z]*$", fname) or re.match("^[a-zA-Z]*$", lname):
            self.amity.add_person(fname, lname, role, wants_accommodation)
        else:        
            cprint("Error. Make sure you only have letters in First name and last name", "red") 

    @docopt_cmd
    def do_allocate_room(self, arg):
        """Usage: allocate_room <id_no> [<accomodation>]"""

        person_id = arg["<id_no>"]
        room = arg["<accomodation>"]
        self.amity.allocate_room(int(person_id), room)

    @docopt_cmd
    def do_reallocate_room(self, arg):
        """ Usage: reallocate_room <id_no> <r_name>"""
        identifier = arg["<id_no>"]
        new_room = arg["<r_name>"]
        self.amity.reallocate_room(int(identifier), new_room)


    @docopt_cmd
    def do_load_people(self, arg):
        """ Usage: load_people [<file_name.txt>]"""

        file_name = arg['<file_name.txt>']
        self.amity.load_people(file_name)


    @docopt_cmd
    def do_print_allocations(self, arg):
        """ Usage: print_allocations [<file_name.txt>] """

        if arg['<file_name.txt>']:
            filename = arg['<file_name.txt>']
        else:
            filename = None
            self.amity.print_allocations(filename)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """ Usage: print_unallocated [<file_name.txt>] """

        if arg['<file_name.txt>']:
            filename = arg['<file_name.txt>']
        else:
            filename = None
            self.amity.print_unallocated(filename)

    @docopt_cmd
    def do_print_room(self, arg):
        """ Usage: print_room <name> """

        room_name = arg['<name>']
        self.amity.print_room(room_name)

    @docopt_cmd
    def do_print_persons(self, arg):
        """ Usage: print_persons [<file_name.txt>] """

        if arg['<file_name.txt>']:
            filename = arg['<file_name.txt>']
        else:
            filename = None
            self.amity.print_persons(filename)

    @docopt_cmd
    def do_delete_person(self, arg):
        """Usage: delete_person <id_no> """

        person_id = arg["<id_no>"]
        self.amity.delete_person(int(person_id))

    @docopt_cmd
    def do_delete_room(self, arg):
        """Usage: delete_room <room_names>..."""

        room_names = arg['<room_names>']
        for room_name in room_names:
            self.amity.delete_room(room_name)

    @docopt_cmd
    def do_save_state(self, arg):
        """ Usage: save_state [<file_name.db>] """

        if not arg['<file_name.db>']:
            dbname = arg['<amity.db>']
        else:
            dbname = arg['<file_name.db>']
            self.amity.save_state(dbname)

    @docopt_cmd
    def do_load_state(self, arg):
        """ Usage: load_state <file_name.db> """

        dbname = arg['<file_name.db>']

        self.amity.load_state(dbname)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        cprint('Good Bye!', "green")
        exit()


opt = docopt(__doc__, sys.argv[1:])


if opt['--interactive']:
    MyInteractive().cmdloop()
    print (opt)
